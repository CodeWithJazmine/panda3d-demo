from direct.actor.Actor import Actor
from panda3d.core import CollisionCapsule, CollisionNode
from panda3d.core import BitMask32, Point3
from direct.interval.IntervalGlobal import Sequence

class Enemy:
    """Handles the enemy actor, movements, and collision"""
    def __init__(self, base):
        self.base = base
        self.base.accept('player-into-enemy', self.handleCollision)

        # === Pacing Panda Actor ===
        # Load and transform the panda actor
        self.pandaActor = Actor("models/panda-model",
                                {"walk": "models/panda-walk4"})
        self.pandaActor.setScale(0.005, 0.005, 0.005)
        self.pandaActor.reparentTo(self.base.render)
        # Loop its animation
        self.pandaActor.loop("walk")

        # === Pacing Panda's Collision (channel 1)===
        cNode = CollisionNode('pacing-panda')
        cNode.addSolid(CollisionCapsule(0,-400,250,0,250,250,300))
        cNode.setFromCollideMask(BitMask32.allOff())
        cNode.setIntoCollideMask(BitMask32.bit(1))
        self.pandaActor.attachNewNode(cNode)

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

    def handleCollision(self, entry):
        self.pandaPace.pause()
        self.pandaActor.stop()
        self.base.StartBattle()