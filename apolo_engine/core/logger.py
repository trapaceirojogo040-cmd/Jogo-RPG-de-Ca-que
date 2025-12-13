# -*- coding: utf-8 -*-
"""
Módulo Logger: Centraliza o registro de todos os eventos e
informações críticas do motor.
"""
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

class MotorLogger:
    """
    Registra eventos críticos de forma estruturada e rastreia o estado do sistema.
    Implementado como um singleton para garantir uma única fonte de verdade para os logs.
    """
    _instancia = None

    def __init__(self):
        self.eventos: List[Dict[str, Any]] = []
        self._max_log = 5000  # Limite de logs para performance
        self.log_path = "apolo_engine.log"

    def registrar(self, origem: str, tipo: str, dados: Dict[str, Any]):
        """
        Cria e armazena um registro de evento com timestamp.

        Args:
            origem (str): Módulo ou sistema que originou o evento (ex: "Combate", "IA").
            tipo (str): Categoria do evento (ex: "dano_recebido", "erro_critico").
            dados (Dict[str, Any]): Dicionário com informações detalhadas.
        """
        evento = {
            "id": str(uuid.uuid4()),
            "origem": origem,
            "tipo": tipo,
            "dados": dados,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.eventos.append(evento)

        # Simulação de gravação assíncrona para não travar o tick do jogo
        if len(self.eventos) % 100 == 0:
            self._escrever_no_disco(evento)

        # Garante que a lista de logs não cresça indefinidamente
        if len(self.eventos) > self._max_log:
            self.eventos = self.eventos[-self._max_log:]

    def _escrever_no_disco(self, evento: Dict[str, Any]):
        """
        Simulação de escrita em disco. Em um ambiente real, isso usaria
        um thread separado ou uma fila para não bloquear a execução principal.
        """
        # Comentado para não gerar I/O real durante a execução em sandbox.
        # with open(self.log_path, "a", encoding="utf-8") as f:
        #     f.write(str(evento) + "\n")
        pass

    def consultar(self, tipo: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Consulta logs por tipo. Se o tipo não for especificado, retorna todos os logs.

        Args:
            tipo (Optional[str]): O tipo de log a ser filtrado.

        Returns:
            List[Dict[str, Any]]: Uma lista de eventos de log.
        """
        if tipo is None:
            return self.eventos
        return [e for e in self.eventos if e["tipo"] == tipo]

# Instância única global para ser importada por outros módulos
LOGGER = MotorLogger()
