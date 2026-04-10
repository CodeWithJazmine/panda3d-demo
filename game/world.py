class World:
    """ Handles the generation of the environment scene"""
    def __init__(self, base):
        self.base = base

        # === Environment Model ===
        scene = self.base.loader.loadModel("models/environment")
        scene.reparentTo(self.base.render)
        scene.setScale(0.25,0.25,0.25)
        scene.setPos(-8,42,0)
