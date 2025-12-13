from panda3d.core import Vec3
from nexus.core.ecs import Component

class Transform(Component):
    def __init__(self, owner, position=Vec3(0,0,0)):
        super().__init__(owner)
        self.position = position
        self.rotation = Vec3(0,0,0)
        self.scale = Vec3(1,1,1)

    def update(self, dt: float):
        """Atualiza o NodePath da entidade com a posição, rotação e escala."""
        self.owner.node.setPos(self.position)
        self.owner.node.setHpr(self.rotation)
        self.owner.node.setScale(self.scale)
