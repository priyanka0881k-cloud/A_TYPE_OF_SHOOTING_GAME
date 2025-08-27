# Forcing a file update to try and clear execution cache.
from direct.showbase.ShowBase import ShowBase
from panda3d.core import (
    AmbientLight, DirectionalLight, Vec4, TextNode, BitMask32,
    CollisionTraverser, CollisionHandlerQueue, CollisionNode, CollisionSphere
)
from direct.gui.OnscreenText import OnscreenText
from game.player import Player
from game.enemy import Enemy

VERSION = "v0.2.2"

from game.constants import PROJECTILE_MASK, ENEMY_MASK

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

        # Enemy manager
        self.enemies = {}
        enemy = Enemy(self, pos=(10, 10, 1))
        self.enemies[str(id(enemy))] = enemy

        # Collision system
        self.cTrav = CollisionTraverser()
        self.cHandler = CollisionHandlerQueue()
        self.taskMgr.add(self.process_collisions, "process_collisions")

        # Projectile manager
        self.projectiles = {}
        self.taskMgr.add(self.update_projectiles, "update_projectiles")

        # Version display
        self.version_text = OnscreenText(
            text=f"Version: {VERSION}",
            pos=(-1.3, 0.95),
            scale=0.05,
            align=TextNode.ALeft
        )

    def update_projectiles(self, task):
        dt = self.taskMgr.globalClock.getDt()
        for p_id, p in list(self.projectiles.items()):
            if not p.update(dt):
                del self.projectiles[p_id]
        return task.cont

    def process_collisions(self, task):
        self.cTrav.traverse(self.render)
        for entry in self.cHandler.getEntries():
            from_node = entry.getFromNodePath().findNetTag("type")
            into_node = entry.getIntoNodePath().findNetTag("type")

            if from_node and into_node:
                if from_node.getTag("type") == "projectile" and into_node.getTag("type") == "enemy":
                    proj_id = from_node.getTag("projectile")
                    enemy_id = into_node.getTag("enemy")

                    if proj_id in self.projectiles:
                        self.projectiles[proj_id].destroy()
                        del self.projectiles[proj_id]

                    if enemy_id in self.enemies:
                        self.enemies[enemy_id].destroy()
                        del self.enemies[enemy_id]

        return task.cont


app = Game()
app.run()
