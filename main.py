import sys
from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3, KeyboardButton, ClockObject, BitMask32
from panda3d.core import CollisionTraverser, CollisionHandlerPusher, CollisionHandlerEvent
from panda3d.core import CollisionSphere, CollisionCapsule, CollisionNode


class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        # === Environment Model ===
        #Load the environment model
        self.scene = self.loader.loadModel("models/environment")
        # Reparent the model to render
        self.scene.reparentTo(self.render)
        # Apply scale and position transforms on model
        self.scene.setScale(0.25,0.25,0.25)
        self.scene.setPos(-8,42,0)
    
        # === Pacing Panda Actor ===
        # Load and transform the panda actor
        self.pandaActor = Actor("models/panda-model",
                                {"walk": "models/panda-walk4"})
        self.pandaActor.setScale(0.005, 0.005, 0.005)
        self.pandaActor.reparentTo(self.render)
        # Loop its animation
        self.pandaActor.loop("walk")

        # === Pacing Panda's Collision (channel 0)===
        cNode = CollisionNode('pacing-panda')
        cNode.addSolid(CollisionCapsule(0,-400,250,0,250,250,300))
        cNode.setFromCollideMask(BitMask32.allOff())
        cNode.setIntoCollideMask(BitMask32.bit(0))
        self.pandaActorC = self.pandaActor.attachNewNode(cNode)
        self.pandaActorC.show()

        # === Pacing Panda's Movements ===
        # Create the four lerp intervals needed for the panda to walk back and forth
        posInterval1 = self.pandaActor.posInterval(13, Point3(0,-10,0), startPos=Point3(0,10,0))
        posInterval2 = self.pandaActor.posInterval(13, Point3(0,10,0), startPos=Point3(0,-10,0))
        hprInterval1 = self.pandaActor.hprInterval(3, Point3(180,0,0), startHpr=Point3(0,0,0))
        hprInterval2 = self.pandaActor.hprInterval(3, Point3(0,0,0), startHpr=Point3(180,0,0))
        # Create and play the sequence that coordinates the intervals
        self.pandaPace = Sequence(posInterval1, hprInterval1, 
                                  posInterval2, hprInterval2,
                                  name="pandaPace")
        self.pandaPace.loop()

        # === Player Actor ===
        # Load another panda to be the player
        self.characterPanda = Actor("models/panda-model",
                                    {"walk": "models/panda-walk4"})
        self.characterPanda.setScale(0.005, 0.005, 0.005)
        self.characterPanda.reparentTo(self.render)
        self.isWalking = False

        # === Player Pusher Collision (channel 0)===
        cNode = CollisionNode('player-pusher')
        cNode.addSolid(CollisionCapsule(0,-400,250,0,250,250,300))
        cNode.setFromCollideMask(BitMask32.bit(0))
        cNode.setIntoCollideMask(BitMask32.allOff())
        self.characterPandaPusher = self.characterPanda.attachNewNode(cNode)
        self.characterPandaPusher.show()

        # === Player Pickup Collision (channel 1)
        cNode = CollisionNode('player-pusher')
        cNode.addSolid(CollisionCapsule(0,-400,250,0,250,250,300))
        cNode.setFromCollideMask(BitMask32.bit(1))
        cNode.setIntoCollideMask(BitMask32.allOff())
        self.characterPandaPickup = self.characterPanda.attachNewNode(cNode)
        
        # === Smiley Model ===
        self.smiley = self.loader.loadModel("models/smiley")
        self.smiley.reparentTo(self.render)
        self.smiley.setPos(5,0,1)

        # === Smiley Pickup Collision (channel 0) ===
        cNode = CollisionNode('smiley')
        cNode.addSolid(CollisionSphere(0,0,0,1.5))
        self.smileyC = self.smiley.attachNewNode(cNode)
        self.smileyC.show()
        cNode.setFromCollideMask(BitMask32.allOff())
        cNode.setIntoCollideMask(BitMask32.bit(1))

        # === Collision Traverser, Pusher, Handler ===
        self.cTrav = CollisionTraverser()

        self.pusher = CollisionHandlerPusher()
        self.cTrav.addCollider(self.characterPandaPusher, self.pusher)
        self.pusher.addCollider(self.characterPandaPusher, self.characterPanda)

        # --- Pickup Interaction ---
        self.handler = CollisionHandlerEvent()
        self.handler.addInPattern("player-into-smiley")
        self.accept('player-into-smiley', self.handle_pickup)
        self.cTrav.addCollider(self.characterPandaPickup, self.handler)


        # === Camera Settings ===
        # Set camera position relative to player Actor
        # and disable mouse control of camera
        self.disableMouse()
        self.camera.setPos(0, 3000, 1300) 
        self.camera.setHpr(180,-10,0)
        self.camLens.setFov(70)
        self.camera.reparentTo(self.characterPanda)
        
        # === Input Settings ===
        self.accept('escape', sys.exit)
        # Register move_task to run every frame via the task manager
        self.task_mgr.add(self.move_task, "moveTask")


    # Called every frame
    # Reads keyboard input and moves player character accordingly
    def move_task(self, task):
        speed = 0.0
        turn_speed = 0.0
       
        is_down = self.mouseWatcherNode.is_button_down

        if is_down(KeyboardButton.up()):
            speed -= 800.0

        if is_down(KeyboardButton.down()):
            speed += 500.0

        if is_down(KeyboardButton.left()):
            turn_speed += 50.0

        if is_down(KeyboardButton.right()):
            turn_speed -= 50.0 

        dt = ClockObject.getGlobalClock().getDt()

        # Animate movement
        is_moving = speed != 0.0 or turn_speed != 0.0
        if is_moving and not self.isWalking:
            self.characterPanda.loop("walk")
            self.isWalking = True
        elif not is_moving and self.isWalking:
            self.characterPanda.stop()
            self.isWalking = False

        y_delta = speed * dt
        self.characterPanda.set_y(self.characterPanda, y_delta)
        self.characterPanda.setH(self.characterPanda, turn_speed * dt)

        return Task.cont

    def handle_pickup(self, entry):
        print(entry)
        self.smiley.removeNode()
        
        
app = MyApp()
app.run()