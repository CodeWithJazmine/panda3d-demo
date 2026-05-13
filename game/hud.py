from panda3d.core import TextNode
from direct.gui.DirectGui import *
from direct.task.Task import Task

class Hud:
    def __init__(self, base):
        self.base = base
        self.resultText = None
        self.bambooBonk = None
        self.leafFlurry = None
        self.zenGuard = None

        # Player Health
        playerHealthNode = TextNode("player health")
        playerHealthNode.setText(f"Player HP: {self.base.player.health}")
        self.playerHealthText = self.base.aspect2d.attachNewNode(playerHealthNode)
        self.playerHealthText.setScale(0.07)
        self.playerHealthText.setPos(-1.3, 0, 0.9)

        # Enemy Health
        enemyHealthNode = TextNode('enemy health')
        enemyHealthNode.setText("Enemy HP: ?")
        self.enemyHealthText = self.base.aspect2d.attachNewNode(enemyHealthNode)
        self.enemyHealthText.setScale(0.07)
        self.enemyHealthText.setPos(-1.3, 0, -0.8)

    def open_battle_hud(self):
        self.bambooBonk = DirectButton(text=("Bamboo Bonk"), 
                             scale=.08, command=self.bamboo_bonk_button)
        self.bambooBonk.setPos(1, 0, -0.5)

        self.leafFlurry = DirectButton(text=("Leaf Flurry"), 
                             scale=.08, command=self.leaf_flurry_button)
        self.leafFlurry.setPos(1, 0, -0.7)
        
        self.zenGuard = DirectButton(text=("Zen Guard"), 
                             scale=.08, command=self.zen_guard_button)
        self.zenGuard.setPos(1, 0, -0.9)

    def close_battle_hud(self):
        self.bambooBonk.destroy()
        self.leafFlurry.destroy()
        self.zenGuard.destroy()

    def bamboo_bonk_button(self):
        self.base.battle_manager.move_chosen("bamboo bonk")

    def leaf_flurry_button(self):
        self.base.battle_manager.move_chosen("leaf flurry")

    def zen_guard_button(self):
        self.base.battle_manager.move_chosen("zen guard")

    def update_health(self):
        self.playerHealthText.node().setText(f"Player HP: {self.base.player.health}")
        self.enemyHealthText.node().setText(f"Enemy HP: {self.base.battle_manager.enemy.health}")

    def disable_buttons(self):
        self.bambooBonk['state'] = DGG.DISABLED
        self.leafFlurry['state'] = DGG.DISABLED
        self.zenGuard['state'] = DGG.DISABLED

    def enable_buttons(self):
        self.bambooBonk['state'] = DGG.NORMAL
        self.leafFlurry['state'] = DGG.NORMAL
        self.zenGuard['state'] = DGG.NORMAL

    def show_turn_result(self, message):
        if self.resultText is not None:
            self.resultText.removeNode()

        text = TextNode('result text')
        text.setText(message)
        self.resultText = self.base.aspect2d.attachNewNode(text)
        self.resultText.setScale(0.07)
        self.resultText.setPos(-0.3, 0, 0.9)

        self.base.taskMgr.doMethodLater(
            2, self._remove_result_text, 'removeResultText'
        )

    def _remove_result_text(self, task):
        if self.resultText is not None:
            self.resultText.removeNode()
            self.resultText = None
        return task.done