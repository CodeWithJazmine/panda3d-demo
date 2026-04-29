from panda3d.core import TextNode
from direct.gui.DirectGui import *

class Hud:
    def __init__(self,  base):
        self.base = base

    def OpenBattleHud(self):
        bambooBonk = DirectButton(text=("Bamboo Bonk"), 
                             scale = .08, command=self.BambooBonkButton)
        bambooBonk.setPos(1, 0, -0.5)

        leafFlurry = DirectButton(text=("Leaf Flurry"), 
                             scale = .08, command=self.ButtonPressed)
        leafFlurry.setPos(1, 0, -0.7)
        
        zenGuard = DirectButton(text=("Zen Guard"), 
                             scale = .08, command=self.ButtonPressed)
        zenGuard.setPos(1, 0, -0.9)

    def ButtonPressed(self):
        print("Button pressed")

    def BambooBonkButton(self):
        self.base.player.BambooBonk()