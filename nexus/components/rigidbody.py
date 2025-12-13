from panda3d.core import Vec3
from panda3d.bullet import BulletRigidBodyNode, BulletBoxShape
from nexus.core.ecs import Component

class RigidBody(Component):
    def __init__(self, owner, mass=1.0):
        super().__init__(owner)
        shape = BulletBoxShape(Vec3(0.5,0.5,0.5))
        self.node = BulletRigidBodyNode(owner.name)
        self.node.setMass(mass)
        self.node.addShape(shape)

    def update(self, dt: float):
        pass
