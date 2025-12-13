import uuid
from typing import Dict, Type
from panda3d.core import NodePath

class Component:
    """Componente base."""
    def __init__(self, owner: 'Entity'):
        self.owner = owner

    def update(self, dt: float):
        pass


class Entity:
    """Entidade genérica (Actor-style Unreal)."""
    def __init__(self, name: str = "Entity"):
        self.id = uuid.uuid4()
        self.name = name
        self.components: Dict[Type[Component], Component] = {}
        self.node = NodePath(name) # Each entity has a NodePath

    def add_component(self, component_cls: Type[Component], *args, **kwargs):
        component = component_cls(self, *args, **kwargs)
        self.components[component_cls] = component
        return component

    def get(self, component_cls: Type[Component]):
        return self.components.get(component_cls)

    def update(self, dt: float):
        for c in self.components.values():
            c.update(dt)

    def get_nodepath(self) -> NodePath:
        return self.node
