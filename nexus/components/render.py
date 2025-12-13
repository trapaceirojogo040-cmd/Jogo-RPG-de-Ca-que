from typing import Optional
from panda3d.core import NodePath
from nexus.core.ecs import Component
from nexus.components.transform import Transform

class RenderComponent(Component):
    """Suporta 2D (UI/sprites) e 3D (models)."""
    def __init__(self, owner, model_path: Optional[str] = None):
        super().__init__(owner)
        self.node: Optional[NodePath] = None
        self.model_path = model_path

    def attach(self, parent: NodePath):
        if self.model_path:
            self.node = parent.attachNewNode(self.owner.name)

    def update(self, dt: float):
        transform = self.owner.get(Transform)
        if self.node and transform:
            self.node.setPos(transform.position)
            self.node.setHpr(transform.rotation)
            self.node.setScale(transform.scale)
