from panda3d.core import TextNode
from direct.gui.DirectGui import *
from direct.task.Task import Task

class Hud:
    def __init__(self,  base):
        self.base = base
        self.countdown = 1

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

    def show_turn_result(self, message):
        # Remove existing text if there is one
        if hasattr(self, 'resultText'):
            self.resultText.removeNode()

        text = TextNode('result text')
        text.setText(message)
        self.resultText = self.base.aspect2d.attachNewNode(text)
        self.resultText.setScale(0.07)
        self.resultText.setPos(-0.3, 0, 0.9)

        # Remove after 2 seconds
        self.base.taskMgr.doMethodLater(
            2, self._remove_result_text, 'removeResultText'
    )

    def _remove_result_text(self, task):
        if hasattr(self, 'resultText'):
            self.resultText.removeNode()
        return task.done