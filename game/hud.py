from panda3d.core import TextNode

class Hud:
    def __init__(self,  base):
        self.base = base

    #     self.count = 0
    #     self.pickupCountText = TextNode('pickup count')
    #     self.pickupCountText.setText(f'pickup count: {self.count}')
    #     pickupCountTextNodePath = self.base.aspect2d.attachNewNode(self.pickupCountText)
    #     pickupCountTextNodePath.setScale(0.07)
    #     pickupCountTextNodePath.setPos(-1.3, 0, 0.9)

    # def incrementPickupCount(self):
    #     self.count += 1
    #     self.pickupCountText.setText(f'pickup count: {self.count}')