from panda3d.core import NodePath, WindowProperties
from .projectile import Projectile

class Player:
    def __init__(self, base):
        self.base = base
        self.player_node = NodePath("player")
        self.player_node.reparentTo(self.base.render)
        self.player_node.setPos(0, 0, 1)

        # Attach camera to player
        self.base.camera.reparentTo(self.player_node)
        self.base.camera.setPos(0, 0, 1.5) # Eye height

        self.model = self.base.loader.loadModel("models/jack")
        self.model.reparentTo(self.player_node)
        # The model will cast shadows automatically.

        self.speed = 10
        self.rotation_speed = 90
        self.key_map = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False,
        }

        self.base.accept("w", self.set_key, ["forward", True])
        self.base.accept("w-up", self.set_key, ["forward", False])
        self.base.accept("s", self.set_key, ["backward", True])
        self.base.accept("s-up", self.set_key, ["backward", False])
        self.base.accept("a", self.set_key, ["left", True])
        self.base.accept("a-up", self.set_key, ["left", False])
        self.base.accept("d", self.set_key, ["right", True])
        self.base.accept("d-up", self.set_key, ["right", False])
        self.base.accept("mouse1", self.shoot)

        self.base.taskMgr.add(self.update, "player_update")
        self.base.taskMgr.add(self.mouse_update, "mouse_update")

        # Mouse control setup
        props = WindowProperties()
        props.setCursorHidden(True)
        props.setMouseMode(WindowProperties.M_RELATIVE)
        self.base.win.requestProperties(props)

    def shoot(self):
        direction = self.base.camera.getQuat(self.base.render).getForward()
        cam_pos = self.base.camera.getPos(self.base.render)
        start_pos = cam_pos + direction * 2  # Start 2 units in front of the camera
        projectile = Projectile(self.base, start_pos, direction)
        self.base.projectiles.append(projectile)


    def set_key(self, key, value):
        self.key_map[key] = value

    def update(self, task):
        dt = self.base.clock.getDt()

        move_vec = self.player_node.getQuat().getForward() * self.speed * dt
        strafe_vec = self.player_node.getQuat().getRight() * self.speed * dt

        if self.key_map["forward"]:
            self.player_node.setPos(self.player_node.getPos() + move_vec)
        if self.key_map["backward"]:
            self.player_node.setPos(self.player_node.getPos() - move_vec)
        if self.key_map["left"]:
            self.player_node.setPos(self.player_node.getPos() - strafe_vec)
        if self.key_map["right"]:
            self.player_node.setPos(self.player_node.getPos() + strafe_vec)

        return task.cont

    def mouse_update(self, task):
        dt = self.base.clock.getDt()
        if self.base.mouseWatcherNode.hasMouse():
            md = self.base.win.getPointer(0)
            x = md.getX()
            y = md.getY()

            # Center mouse
            self.base.win.movePointer(0, self.base.win.getXSize() // 2, self.base.win.getYSize() // 2)

            # Player heading
            self.player_node.setH(self.player_node.getH() - (x - self.base.win.getXSize() / 2) * self.rotation_speed * dt)

            # Camera pitch
            new_pitch = self.base.camera.getP() - (y - self.base.win.getYSize() / 2) * self.rotation_speed * dt
            self.base.camera.setP(max(-90, min(90, new_pitch)))

        return task.cont
