from panda3d.core import CollisionSphere, CollisionNode, BitMask32

class Pickup:
    """ Handles the pickup item and its collsion"""
    def __init__(self, base):
        self.base = base

        # === Smiley Model ===
        smiley = self.base.loader.loadModel("models/smiley")
        smiley.reparentTo(self.base.render)
        smiley.setPos(5,0,1)

        # === Smiley Pickup Collision (channel 0) ===
        cNode = CollisionNode('smiley')
        cNode.addSolid(CollisionSphere(0,0,0,1.5))
        smileyC = smiley.attachNewNode(cNode)
        smileyC.show()
        cNode.setFromCollideMask(BitMask32.allOff())
        cNode.setIntoCollideMask(BitMask32.bit(1))