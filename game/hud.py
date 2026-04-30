from panda3d.core import TextNode
from direct.gui.DirectGui import *

class Hud:
    def __init__(self,  base):
        self.base = base

    def open_battle_hud(self):
        self.bambooBonk = DirectButton(text=("Bamboo Bonk"), 
                             scale = .08, command=self.bamboo_bonk_button)
        self.bambooBonk.setPos(1, 0, -0.5)

        self.leafFlurry = DirectButton(text=("Leaf Flurry"), 
                             scale = .08, command=self.leaf_flurry_button)
        self.leafFlurry.setPos(1, 0, -0.7)
        
        self.zenGuard = DirectButton(text=("Zen Guard"), 
                             scale = .08, command=self.zen_guard_button)
        self.zenGuard.setPos(1, 0, -0.9)

    def close_battle_hud(self):
        self.bambooBonk.destroy()
        self.leafFlurry.destroy()
        self.zenGuard.destroy()

    def button_pressed(self):
        print("Button pressed")

    def bamboo_bonk_button(self):
        self.base.battle_manager.move_chosen("bamboo bonk")

    def leaf_flurry_button(self):
        self.base.battle_manager.move_chosen("leaf flurry")

    def zen_guard_button(self):
        self.base.battle_manager.move_chosen("zen guard")