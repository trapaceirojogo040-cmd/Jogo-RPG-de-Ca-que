from panda3d.core import loadPrcFileData
loadPrcFileData('', 'window-type none') # Não criar uma janela gráfica
loadPrcFileData('', 'audio-library-name p3openal_audio') # Usar OpenAL para áudio

from nexus.core.game import NexusGame
from nexus.core.ecs import Entity
from nexus.components.transform import Transform
from nexus.components.ai import AIComponent
from nexus.components.audio import AudioComponent
from nexus.utils.logger import logger

if __name__ == "__main__":
    logger.info("Inicializando NEXUS HYBRID ENGINE")
    game = NexusGame()

    # Criar a entidade do jogador
    player = Entity("Player")

    # Adicionar componentes
    player.add_component(Transform)
    player.add_component(AIComponent)
    audio_component = player.add_component(AudioComponent, game.audio)

    # Adicionar e tocar um som
    audio_component.add_sound("test_sound", "assets/test_sound.wav")
    audio_component.play("test_sound")

    # Adicionar a entidade ao jogo
    game.add_entity(player)

    # O jogo não precisa de game.run() em modo headless para este teste,
    # a inicialização já é suficiente para testar o áudio.
    # Se precisássemos do loop, usaríamos taskMgr.step()
    logger.info("Teste de áudio concluído.")
