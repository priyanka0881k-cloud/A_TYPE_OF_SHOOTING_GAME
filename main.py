from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight, DirectionalLight, Vec4
from game.player import Player


class Game(ShowBase):
    def __init__(self):
        super().__init__()

        # Load the environment model.
        self.scene = self.loader.loadModel("models/environment")
        # Reparent the model to render.
        self.scene.reparentTo(self.render)
        # Apply scale and position transformations on the model.
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        # Add lighting
        alight = AmbientLight('alight')
        alight.setColor(Vec4(0.2, 0.2, 0.2, 1))
        alnp = self.render.attachNewNode(alight)
        self.render.setLight(alnp)

        dlight = DirectionalLight('dlight')
        dlight.setColor(Vec4(0.8, 0.8, 0.5, 1))
        dlight.setShadowCaster(True, 512, 512)
        dlnp = self.render.attachNewNode(dlight)
        dlnp.setHpr(0, -60, 0)
        self.render.setLight(dlnp)

        # The scene will cast shadows automatically.

        # Enable the shader generator
        self.render.setShaderAuto()

        # Disable the default mouse camera control.
        self.disableMouse()

        # Create a player instance.
        self.player = Player(self)

        # Projectile manager
        self.projectiles = []
        self.taskMgr.add(self.update_projectiles, "update_projectiles")

    def update_projectiles(self, task):
        dt = self.taskMgr.globalClock.getDt()
        for p in list(self.projectiles):
            if not p.update(dt):
                self.projectiles.remove(p)
        return task.cont


app = Game()
app.run()
