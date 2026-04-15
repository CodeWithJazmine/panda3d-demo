from direct.actor.Actor import Actor
from panda3d.core import CollisionCapsule, CollisionNode
from panda3d.core import BitMask32, Point3
from direct.interval.IntervalGlobal import Sequence

class Enemy:
    """Handles the enemy actor, movements, and collision"""
    def __init__(self, base):
        self.base = base

        # === Pacing Panda Actor ===
        # Load and transform the panda actor
        pandaActor = Actor("models/panda-model",
                                {"walk": "models/panda-walk4"})
        pandaActor.setScale(0.005, 0.005, 0.005)
        pandaActor.reparentTo(self.base.render)
        # Loop its animation
        pandaActor.loop("walk")

        # === Pacing Panda's Collision (channel 0)===
        cNode = CollisionNode('pacing-panda')
        cNode.addSolid(CollisionCapsule(0,-400,250,0,250,250,300))
        cNode.setFromCollideMask(BitMask32.allOff())
        cNode.setIntoCollideMask(BitMask32.bit(0))
        pandaActor.attachNewNode(cNode)

         # === Pacing Panda's Movements ===
        # Create the four lerp intervals needed for the panda to walk back and forth
        posInterval1 = pandaActor.posInterval(13, Point3(0,-10,0), startPos=Point3(0,10,0))
        posInterval2 = pandaActor.posInterval(13, Point3(0,10,0), startPos=Point3(0,-10,0))
        hprInterval1 = pandaActor.hprInterval(3, Point3(180,0,0), startHpr=Point3(0,0,0))
        hprInterval2 = pandaActor.hprInterval(3, Point3(0,0,0), startHpr=Point3(180,0,0))
        # Create and play the sequence that coordinates the intervals
        pandaPace = Sequence(posInterval1, hprInterval1, 
                                  posInterval2, hprInterval2,
                                  name="pandaPace")
        pandaPace.loop()