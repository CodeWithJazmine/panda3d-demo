from direct.showbase.ShowBase import ShowBase
from .player import Player
from .world import World
from .enemy import Enemy
from .pickup import Pickup
from .hud import Hud
from .battleManager import BattleManager

class Game(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.player = Player(self)
        self.world = World(self)
        self.enemy = Enemy(self)
        self.hud = Hud(self)
        self.battle_manager = BattleManager(self)

        # positions = [(5,0,1), (10,5,1), (-5,5,1), (-10, 0, 1)]
        # self.pickups = []
        # for pos in positions:
        #     pickup = Pickup(self, pos)
        #     self.pickups.append(pickup)
        

    def game_over(self):
        #TODO: create a game over text popup in Hud
        print("Game over")
        self.player.disable_move()

