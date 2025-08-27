from panda3d.core import NodePath, CollisionNode, CollisionSphere
from .constants import PROJECTILE_MASK, ENEMY_MASK

class Projectile:
    def __init__(self, base, start_pos, direction):
        self.base = base
        self.start_pos = start_pos
        self.direction = direction
        self.speed = 50
        self.lifetime = 5  # seconds
        self.age = 0

        self.model = self.base.loader.loadModel("models/misc/sphere")
        self.model.reparentTo(self.base.render)
        self.model.setPos(start_pos)
        self.model.setScale(0.1)
        self.model.setTag("type", "projectile")
        self.model.setTag("projectile", str(id(self)))


        # Collision setup
        cnode = CollisionNode('projectile_cnode')
        cnode.addSolid(CollisionSphere(0, 0, 0, 0.3))
        cnode.setFromCollideMask(PROJECTILE_MASK)
        cnode.setIntoCollideMask(0) # Projectiles don't get hit
        self.cpath = self.model.attachNewNode(cnode)
        self.base.cTrav.addCollider(self.cpath, self.base.cHandler)

    def update(self, dt):
        self.age += dt
        if self.age > self.lifetime:
            self.destroy()
            return False  # Signal to remove this projectile

        self.model.setPos(self.model.getPos() + self.direction * self.speed * dt)
        return True # Signal to keep this projectile

    def destroy(self):
        self.base.cTrav.removeCollider(self.cpath)
        self.model.removeNode()
