
class BattleManager:
    def __init__(self, base):
        self.base = base
        self.playersTurn = True

    def start_battle(self, enemy):
        self.enemy = enemy
        self.base.player.disable_move()

        self.player_turn()
    
    def end_battle(self):
        self.base.player.enable_move()
        self.base.hud.close_battle_hud()
    
    def player_turn(self):
        self.base.hud.open_battle_hud()
        self.playersTurn = True

    def move_chosen(self, move):
        if move == "bamboo bonk":
            self.base.player.bamboo_bonk(self.enemy)
        elif move == "leaf flurry":
            self.base.player.leaf_flurry(self.enemy)
        elif move == "zen guard":
            self.base.player.zen_guard(self.enemy)

        self.check_battle_state("enemy")

    def enemy_turn(self):
        self.playersTurn = False
        self.base.hud.close_battle_hud()
        #TODO: create enemy ai attacks, for now...
        self.base.player.take_damage(1)

        self.check_battle_state("player")

    def check_battle_state(self, turn):
        if turn == "player":
            if self.base.player.is_alive():
                self.player_turn()
            else:
                self.end_battle()
                self.base.game_over()

        elif turn == "enemy":
            if self.enemy.is_alive():
                # Wait 2 seconds before enemy attacks
                self.base.taskMgr.doMethodLater(2,self._do_enemy_turn, 'enemyTurn')
               
            else:
                self.enemy.die()
                self.end_battle()

    def _do_enemy_turn(self, task):
        self.enemy_turn()
        return task.done


    
    

