# -*- coding: utf-8 -*-
"""
Ponto de Entrada Principal para o Apolo Engine (v2.0).

Este arquivo demonstra como inicializar o motor, configurar um cenário
de jogo com múltiplas entidades (incluindo IA) e executar uma simulação
para observar o comportamento dinâmico do sistema.
"""
import time
import random

from apolo_engine.motor import MOTOR
from apolo_engine.entities.entidade import Entidade
from apolo_engine.core.logger import LOGGER # Importar o logger

def configurar_cenario():
    """
    Cria e registra as entidades iniciais, configurando o mundo do jogo.
    """
    print("--- Configurando Cenário (v2.0) ---")

    # Criar um jogador principal
    jogador = Entidade(nome="Caíque", nivel=10, classe="Jogador")
    MOTOR.registrar_entidade(jogador, controlada_por_ia=False)

    # Criar alguns NPCs para interagir
    npc_aliado = Entidade(nome="Eva-7K", nivel=8, classe="Aliado")
    MOTOR.registrar_entidade(npc_aliado, controlada_por_ia=True)

    npc_inimigo = Entidade(nome="Nexus Corrompido", nivel=12, classe="Inimigo")
    MOTOR.registrar_entidade(npc_inimigo, controlada_por_ia=True)

    # Posicionar entidades aleatoriamente no mundo
    for entidade_id in MOTOR.entidades.keys():
        corpo = MOTOR.fisica.corpos.get(entidade_id)
        if corpo:
            corpo.posicao.x = random.uniform(-50, 50)
            corpo.posicao.y = random.uniform(-50, 50)

    print("Cenário configurado: 1 Jogador, 2 NPCs (IA).")
    print("-----------------------------------\n")

def executar_simulacao(numero_de_ticks: int):
    """
    Executa o loop principal do jogo por um número determinado de ticks.
    """
    print(f"--- Iniciando Simulação ({numero_de_ticks} Ticks) ---")

    for i in range(numero_de_ticks):
        print(f"\n[TICK {i+1}/{numero_de_ticks}]")
        MOTOR.tick()

        # Exibe o estado de todas as entidades vivas
        for entidade in MOTOR.entidades.values():
            if entidade.esta_viva():
                pos = MOTOR.fisica.corpos[entidade.id].posicao
                print(f"  - {entidade} | Posição: {pos}")

        time.sleep(0.5) # Pausa para facilitar a leitura

        # Condição de parada (se todos os NPCs morrerem)
        npcs_vivos = [e for e in MOTOR.entidades.values() if e.classe != "Jogador" and e.esta_viva()]
        if not npcs_vivos:
            print("\nTodos os NPCs foram derrotados! Fim da simulação.")
            break

    print("\n--- Simulação Encerrada ---")

def exibir_relatorio_final():
    """
    Mostra as estatísticas finais do motor e dos subsistemas.
    """
    print("\n--- Relatório Final do Motor ---")
    stats = MOTOR.obter_estatisticas()

    print(f"\n[Log]")
    log_stats = stats["log"]
    print(f"  - Total de registros: {log_stats['total']}")
    print(f"  - Tipos de eventos registrados: {list(log_stats['tipos'].keys())}")

    print(f"\n[Eventos]")
    evento_stats = stats["eventos"]
    print(f"  - Eventos na fila: {evento_stats['eventos_na_fila']}")
    print(f"  - Total de eventos com assinantes: {evento_stats['eventos_com_assinantes']}")

    print("\n[Entidades Destruídas]")
    # Filtra os logs de eventos, procurando por aqueles cujo nome do evento é 'ENTIDADE_DESTRUIDA'
    logs_morte = [
        log for log in MOTOR.logger.consultar(tipo="evento_disparado")
        if log['dados'].get('nome') == 'ENTIDADE_DESTRUIDA'
    ]
    if not logs_morte:
        print("  - Nenhuma entidade foi destruída.")
    for log in logs_morte:
        # A informação da entidade morta está dentro do campo 'dados' do próprio evento
        info_morte = log['dados'].get('dados', {})
        print(f"  - {info_morte.get('nome', 'Nome não encontrado')} (ID: {info_morte.get('id', 'ID não encontrado')})")
    print("-----------------------------------\n")


def main():
    """
    Função principal que orquestra a demonstração.
    """
    try:
        MOTOR.iniciar()
        configurar_cenario()
        executar_simulacao(numero_de_ticks=15)
        exibir_relatorio_final()
    except Exception as e:
        print(f"\nERRO CRÍTICO NO MOTOR: {e}")
        LOGGER.registrar("main", "erro_critico", {"erro": str(e)})

if __name__ == "__main__":
    main()
