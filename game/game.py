from direct.showbase.ShowBase import ShowBase
from panda3d.core import TextNode
from .player import Player
from .world import World
from .enemy import Enemy
from .pickup import Pickup

class Game(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.player = Player(self)
        self.world = World(self)
        self.enemy = Enemy(self)

        positions = [(5,0,1), (10,5,1), (-5,5,1), (-10, 0, 1)]
        self.pickups = []
        for pos in positions:
            pickup = Pickup(self, pos)
            self.pickups.append(pickup)


