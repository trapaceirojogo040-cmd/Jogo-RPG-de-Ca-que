# -*- coding: utf-8 -*-
"""
Ponto de Entrada Principal para o Motor Apolo.

Este arquivo demonstra como inicializar o motor, configurar um cenário
de jogo simples e executar o loop de simulação.
"""
import time

from apolo_engine.motor import ApoloEngine
from apolo_engine.entities.entidade_base import EntidadeBase
from apolo_engine.core.logger import LOGGER

def configurar_cenario(motor: ApoloEngine):
    """
    Cria e registra as entidades iniciais do jogo.
    """
    LOGGER.registrar("main", "config_cenario", {"mensagem": "Configurando cenário..."})

    # Criar personagens
    guerreiro = EntidadeBase(nome="Kael", nivel=10, classe="Guerreiro")
    arqueira = EntidadeBase(nome="Mira", nivel=8, classe="Arqueira")

    # Ajustar atributos para a demonstração
    guerreiro.ataque = 55
    arqueira.hp_max = 120
    arqueira.hp_atual = 120

    # Registrar entidades no motor
    motor.registrar_entidade(guerreiro)
    motor.registrar_entidade(arqueira)

    # Posicionar entidades no mundo (usando o sistema de física)
    motor.fisica.corpos[guerreiro.id].posicao.x = 10
    motor.fisica.corpos[arqueira.id].posicao.y = 5

    LOGGER.registrar("main", "config_cenario", {"mensagem": "Cenário configurado com sucesso."})


def main():
    """
    Função principal que inicializa e executa o motor.
    """
    print("--- INICIANDO MOTOR APOLO ENGINE ---")
    motor = ApoloEngine()

    configurar_cenario(motor)

    # Exemplo de ataque para gerar logs
    guerreiro = [e for e in motor.entidades.values() if e.nome == "Kael"][0]
    arqueira = [e for e in motor.entidades.values() if e.nome == "Mira"][0]
    motor.combate.executar_ataque(guerreiro, arqueira)

    print("\n--- INICIANDO LOOP DE SIMULAÇÃO (10 TICKS) ---")
    try:
        for i in range(10):
            print(f"\n[TICK {i+1}]")
            motor.tick()

            # Imprimir o estado das entidades
            for entidade in motor.entidades.values():
                pos = motor.fisica.corpos[entidade.id].posicao
                print(f"  - {entidade} | Posição: {pos}")

            # Simula um pequeno atraso para o loop não ser instantâneo
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nLoop interrompido pelo usuário.")
    finally:
        print("\n--- SIMULAÇÃO ENCERRADA ---")
        motor.encerrar()

        # Exibir logs de dano para verificação
        print("\nLogs de Dano Registrados:")
        logs_dano = LOGGER.consultar("dano")
        for log in logs_dano:
            print(f"  - {log['origem']} causou {log['dados']['dano']:.1f} de dano.")

if __name__ == "__main__":
    main()
