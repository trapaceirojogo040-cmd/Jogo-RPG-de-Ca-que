from typing import Dict
from nexus.core.ecs import Component
from nexus.systems.audio import AudioManager

class AudioComponent(Component):
    """Componente para adicionar sons a uma entidade."""
    def __init__(self, owner, audio_manager: AudioManager):
        super().__init__(owner)
        self.audio_manager = audio_manager
        self.sounds: Dict[str, str] = {}

    def add_sound(self, name: str, path: str):
        """Adiciona um som ao componente e o carrega no AudioManager."""
        self.sounds[name] = path
        self.audio_manager.load_sound(name, path)

    def play(self, name: str):
        """Toca um som associado a esta entidade."""
        if name in self.sounds:
            self.audio_manager.play_3d(name, self.owner.get_nodepath()) # Assuming the entity has a NodePath
