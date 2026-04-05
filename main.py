import sys
from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3
from panda3d.core import KeyboardButton
from panda3d.core import ClockObject
from panda3d.core import CollisionTraverser, CollisionHandlerPusher
from panda3d.core import CollisionSphere, CollisionNode


class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        #Load the environment model
        self.scene = self.loader.loadModel("models/environment")
        # Reparent the model to render
        self.scene.reparentTo(self.render)
        # Apply scale and position transforms on model
        self.scene.setScale(0.25,0.25,0.25)
        self.scene.setPos(-8,42,0)
    
        # Load and transform the panda actor
        self.pandaActor = Actor("models/panda-model",
                                {"walk": "models/panda-walk4"})
        self.pandaActor.setScale(0.005, 0.005, 0.005)
        self.pandaActor.reparentTo(self.render)
        # Loop its animation
        self.pandaActor.loop("walk")

        # --- Pacing Panda's Collision ---
        # Create a collision node for the pacing panda
        cNode = CollisionNode('pacing-panda')
        # Attach a collision sphere to the collision node
        cNode.addSolid(CollisionSphere(0,-130,250,520))
        # Attach the collsion node to the pacing panda's model
        self.pandaActorC = self.pandaActor.attachNewNode(cNode)
        # Set the pacing panda's collision node to render as visible
        self.pandaActorC.show()

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

        # Load another panda to be the player
        self.characterPanda = Actor("models/panda-model",
                                    {"walk": "models/panda-walk4"})
        self.characterPanda.setScale(0.005, 0.005, 0.005)
        self.characterPanda.reparentTo(self.render)
        self.isWalking = False


         # --- Player's Collision ----
        # Create a collision node for player model
        cNode = CollisionNode('player')
        # Attach  a collsion sphere to the collision node
        cNode.addSolid(CollisionSphere(0,-130,250,520))
        # Attach the collision node to the player's model
        self.characterPandaC = self.characterPanda.attachNewNode(cNode)
        # Set the player's collision node to render as visible
        self.characterPandaC.show()
        
        # --- Collision Pusher ---
        self.cTrav = CollisionTraverser()
        pusher = CollisionHandlerPusher()
        self.cTrav.addCollider(self.characterPandaC, pusher)
        pusher.addCollider(self.characterPandaC, self.characterPanda, self.drive.node())
        
        # Set camera position relative to player Actor
        # and disable mouse control of camera
        self.disableMouse()
        self.camera.setPos(0, 3000, 1300) 
        self.camera.setHpr(180,-10,0)
        self.camLens.setFov(70)
        self.camera.reparentTo(self.characterPanda)
        
        # Input 
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

        
app = MyApp()
app.run()