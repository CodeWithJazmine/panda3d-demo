from panda3d.core import CollisionSphere, CollisionNode, BitMask32
from direct.showbase import DirectObject

class Pickup(DirectObject.DirectObject):
    """ Handles the pickup item and its collision"""
    def __init__(self, base, pos=(5,0,1)):
        self.base = base
        self.accept('player-pickup-into-smiley', self.handlePickup)

        # === Smiley Model ===
        self.smiley = self.base.loader.loadModel("models/smiley")
        self.smiley.reparentTo(self.base.render)
        self.smiley.setPos(*pos)

        # === Smiley Pickup Collision (channel 0) ===
        cNode = CollisionNode('smiley')
        cNode.addSolid(CollisionSphere(0,0,0,1.5))
        self.smiley.attachNewNode(cNode)
        cNode.setFromCollideMask(BitMask32.allOff())
        cNode.setIntoCollideMask(BitMask32.bit(1))
        
    def handlePickup(self, entry):
        hit = entry.getIntoNodePath().getParent()
        if hit == self.smiley:
            self.smiley.removeNode()
            self.destroy()

    def destroy(self):
        self.ignoreAll()