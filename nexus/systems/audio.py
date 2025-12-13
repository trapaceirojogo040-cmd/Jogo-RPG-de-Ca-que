from typing import Dict
from direct.showbase.ShowBase import ShowBase

class AudioManager:
    """Gerencia o carregamento e a reprodução de sons."""
    def __init__(self, base: ShowBase):
        self.base = base
        self.sounds: Dict[str, any] = {}

    def load_sound(self, name: str, path: str):
        """Carrega um som e o armazena para uso posterior."""
        sound = self.base.loader.loadSfx(path)
        self.sounds[name] = sound
        return sound

    def play_2d(self, name: str):
        """Toca um som 2D (não posicional)."""
        if name in self.sounds:
            self.sounds[name].play()

    def play_3d(self, name: str, node):
        """Toca um som 3D (posicional)."""
        if name in self.sounds:
            sound = self.sounds[name]
            sound.set_3d_attributes(node.getX(), node.getY(), node.getZ(), 0, 0, 0)
            sound.play()
