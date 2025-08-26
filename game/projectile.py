from panda3d.core import NodePath

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

    def update(self, dt):
        self.age += dt
        if self.age > self.lifetime:
            self.destroy()
            return False  # Signal to remove this projectile

        self.model.setPos(self.model.getPos() + self.direction * self.speed * dt)
        return True # Signal to keep this projectile

    def destroy(self):
        self.model.removeNode()
