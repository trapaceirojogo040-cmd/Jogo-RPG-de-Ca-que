import time
from typing import List
from direct.showbase.ShowBase import ShowBase
from nexus.core.ecs import Entity
from nexus.systems.physics import PhysicsWorld
from nexus.systems.audio import AudioManager

class NexusGame(ShowBase):
    """Loop principal estilo Unreal (Tick)."""
    def __init__(self):
        super().__init__()
        self.disableMouse()
        self.entities: List[Entity] = []
        self.physics = PhysicsWorld()
        self.audio = AudioManager(self)
        self.last_time = time.time()
        self.taskMgr.add(self.game_loop, "NexusLoop")

    def add_entity(self, entity: Entity):
        self.entities.append(entity)
        entity.get_nodepath().reparentTo(self.render)

    def game_loop(self, task):
        now = time.time()
        dt = now - self.last_time
        self.last_time = now

        for e in self.entities:
            e.update(dt)

        self.physics.step(dt)
        return task.cont
