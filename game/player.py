import sys
from direct.task import Task 
from direct.actor.Actor import Actor
from panda3d.core import CollisionCapsule, CollisionNode
from panda3d.core import CollisionTraverser, CollisionHandlerPusher, CollisionHandlerEvent
from panda3d.core import KeyboardButton, ClockObject, BitMask32

class Player:
    """Handles player actor, movement, animation, and collision."""
    def __init__(self, base):
        self.base = base

        # === Player Actor ===
        # Load another panda to be the player
        self.characterPanda = Actor("models/panda-model",
                                         {"walk": "models/panda-walk4"})
        self.characterPanda.setScale(0.005, 0.005, 0.005)
        self.characterPanda.reparentTo(self.base.render)
        self.isWalking = False

        # === Player Pusher Collision (channel 0)===
        cNode = CollisionNode('player-pusher')
        cNode.addSolid(CollisionCapsule(0,-400,250,0,250,250,300))
        cNode.setFromCollideMask(BitMask32.bit(0))
        cNode.setIntoCollideMask(BitMask32.allOff())
        characterPandaPusher = self.characterPanda.attachNewNode(cNode)
        characterPandaPusher.show()

        # === Player Pickup Collision (channel 1)
        cNode = CollisionNode('player-pickup')
        cNode.addSolid(CollisionCapsule(0,-400,250,0,250,250,300))
        cNode.setFromCollideMask(BitMask32.bit(1))
        cNode.setIntoCollideMask(BitMask32.allOff())
        characterPandaPickup = self.characterPanda.attachNewNode(cNode)
        
        # === Collision Traverser, Pusher, Handler ===
        self.base.cTrav = CollisionTraverser()

        pusher = CollisionHandlerPusher()
        self.base.cTrav.addCollider(characterPandaPusher, pusher)
        pusher.addCollider(characterPandaPusher, self.characterPanda)

        # --- Pickup Interaction ---
        # Create a event notification when player collides with smiley
        handler = CollisionHandlerEvent()
        handler.addInPattern("player-pickup-into-smiley")
        self.base.cTrav.addCollider(characterPandaPickup, handler)


        # === Camera Settings ===
        # Set camera position relative to player Actor
        # and disable mouse control of camera
        self.base.disableMouse()
        self.base.camera.setPos(0, 3000, 1300) 
        self.base.camera.setHpr(180,-10,0)
        self.base.camLens.setFov(70)
        self.base.camera.reparentTo(self.characterPanda)
        
        # === Input Settings ===
        self.base.accept('escape', sys.exit) # Does Panda3D have a way to close the program?
        # Register move_task to run every frame via the task manager
        self.base.task_mgr.add(self.move_task, "moveTask")       


    # Called every frame
    # Reads keyboard input and moves player character accordingly
    def move_task(self, task):
        speed = 0.0
        turn_speed = 0.0
       
        is_down = self.base.mouseWatcherNode.is_button_down

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