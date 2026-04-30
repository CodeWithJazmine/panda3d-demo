class BattleManager:
    def __init__(self, base):
        self.base = base

    def start_battle(self, enemy):
        self.enemy = enemy
        self.base.player.disable_move()
        self.base.hud.open_battle_hud()
    
    def end_battle(self):
        self.base.player.enable_move()
        self.base.hud.close_battle_hud()
    
    def move_chosen(self, move):
        if move == "bamboo bonk":
            self.base.player.bamboo_bonk(self.enemy)
        elif move == "leaf flurry":
            self.base.player.leaf_flurry(self.enemy)
        elif move == "zen guard":
            self.base.player.zen_guard(self.enemy)
    

