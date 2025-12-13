from typing import Optional
from nexus.core.ecs import Component

class AIState:
    def enter(self, entity): pass
    def update(self, entity, dt): pass
    def exit(self, entity): pass


class AIComponent(Component):
    def __init__(self, owner):
        super().__init__(owner)
        self.state: Optional[AIState] = None

    def set_state(self, state: AIState):
        if self.state:
            self.state.exit(self.owner)
        self.state = state
        self.state.enter(self.owner)

    def update(self, dt: float):
        if self.state:
            self.state.update(self.owner, dt)
