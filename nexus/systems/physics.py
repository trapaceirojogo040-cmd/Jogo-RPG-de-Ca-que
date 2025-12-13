from panda3d.core import Vec3
from panda3d.bullet import BulletWorld

class PhysicsWorld:
    def __init__(self):
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))

    def step(self, dt: float):
        self.world.doPhysics(dt)
