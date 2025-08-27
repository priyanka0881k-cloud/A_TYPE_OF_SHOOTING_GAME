from panda3d.core import NodePath, CollisionNode, CollisionCapsule
from .constants import ENEMY_MASK

class Enemy:
    def __init__(self, base, pos):
        self.base = base

        self.model = self.base.loader.loadModel("models/jack")
        self.model.reparentTo(self.base.render)
        self.model.setPos(pos)
        self.model.setTag("type", "enemy")
        self.model.setTag("enemy", str(id(self)))


        # Collision setup
        # Using a capsule for the character shape
        cnode = CollisionNode('enemy_cnode')
        cnode.addSolid(CollisionCapsule(0, 0, 1, 0, 0, 4, 0.5))
        cnode.setIntoCollideMask(ENEMY_MASK)
        self.cpath = self.model.attachNewNode(cnode)

    def destroy(self):
        self.model.removeNode()
