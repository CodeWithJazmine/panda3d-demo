from direct.showbase.ShowBase import ShowBase
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
        self.pickup = Pickup(self)
