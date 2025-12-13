from nexus.core.ecs import Entity
from nexus.components.transform import Transform
from panda3d.core import Vec3

def test_entity_component():
    """Testa a criação de uma entidade e a adição de um componente."""
    e = Entity("Test")
    t = e.add_component(Transform)
    assert t is not None
    assert t.position == Vec3(0, 0, 0)
