# =============== ARQUIVO CONCEITO: SUPREMO_RPG_IA_X_FINAL.py ===============
# Arquitetura Unificada de RPG de Estratégia, Hierarquia, Economia e Protocolo IA.
# O foco é na interdependência dos módulos: Tecnologia afeta Protocolo e Economia.

import random
import uuid
import math
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any

# 1. --- MÓDULO DE SEGURANÇA E PODER PSICOLÓGICO ---
class ProtocoloDePoder:
    """Define a Volição e Sinergia dos personagens."""
    def __init__(self, cargo: str):
        self.volicao_level: int = random.randint(50, 100)
        self.sinergia_moral: float = 1.0
        self.habilidades = self._set_habilidades(cargo)

    def _set_habilidades(self, cargo: str) -> Dict[str, str]:
        if "PROPRIETÁRIO" in cargo or "Comandante" in cargo:
            self.volicao_level = 999
            self.sinergia_moral = 1.5
            return {
                "Poder Psicológico": "Volição (Controle de Causalidade OP)",
                "Força Bélica": "Arsenal de Éter e Defesa Quântica",
            }
        return {"Poder Psicológico": "Padrão", "Força Bélica": "Básico"}

class ServicoDeArmazenamento:
    """Gerencia o armazenamento seguro e o protocolo de destruição de dados."""
    def __init__(self):
        self.logins: Dict[str, datetime] = {}

    def executar_protocolo_de_entropia(self, max_days_inactive: int = 30):
        """Executa a Lei da Destruição de Dados (Entropia)."""
        cutoff_date = datetime.now() - timedelta(days=max_days_inactive)
        keys_to_destroy = [
            user_id for user_id, last_login in self.logins.items()
            if last_login < cutoff_date
        ]
        for user_id in keys_to_destroy:
            del self.logins[user_id]
            print(f" [PROTOCOLO ENTROPIA]: Dados de {user_id[:8]} destruídos por inatividade.")

# 2. --- CONFIGURAÇÃO GLOBAL E HIERARQUIA ---
CLASSES = ['Guerreiro', 'Mago', 'Comandante', 'Engenheiro', 'Assassino', 'Espadachim', 'Clérigo']
RACAS = ['Humano', 'Elfo', 'Orc', 'Demônio', 'Androide', 'IA']
ARMAS = ['Espada Laser', 'Fuzil de Plasma', 'Varinha Arcana', 'Canhão Orbital']
TECNOLOGIAS = ['Campo de Força Quântico', 'Nanobots de Reparo', 'Bombardeio Orbital', 'Teleportador Tático', 'IA Defensiva']
CARGOS = ['PROPRIETÁRIO', 'Administrador', 'Diretor', 'Master GM', 'Mestre de Jogo', 'Moderador', 'Jogador']

# Definições de Comportamento Militar
PHRASES_MILITARES: Dict[str, str] = {
    "ATAQUE_TOTAL": "O preço da vitória é a preparação",
    "RECUO_ESTRATEGICO": "Reagrupar é prioridade, a força retornará",
    "DEFESA_IMEDIATA": "Linhas de defesa ativas, posição mantida",
}
COMPORTAMENTO_STATUS: Dict[str, Dict[str, Any]] = {
    "AGRESSIVO": {"risco": 0.8, "consumo_recursos": 1.5, "bônus_dano": 0.2},
    "DEFENSIVO": {"risco": 0.2, "consumo_recursos": 0.5, "bônus_defesa": 0.3},
    "NEUTRO": {"risco": 0.5, "consumo_recursos": 1.0},
}

# Ações Militares que requerem Protocolo de Confirmação (Frases de Comportamento)
ACOES_MILITARES = {
    "ASSALTO_FINAL": {"risco": 0.9, "consumo_eter": 50, "recompensa_xp": 500},
    "REAGRUPAMENTO": {"risco": 0.1, "consumo_eter": 10, "recompensa_xp": 50},
    "DESCOBERTA_PLANETA": {"risco": 0.5, "consumo_eter": 30, "recompensa_xp": 250},
    "ATAQUE_TOTAL": {"risco": 0.8, "consumo_eter": 40, "recompensa_xp": 400}
}
SENHA_BASE = "edson4020SS" # Base para geração do código de confirmação

def rank_xp(xp):
    """Calcula a Patente de poder (F, E, C, B, A, S, Lenda) baseado na XP total."""
    limites = [100, 500, 2500, 8000, 30000, 70000, 99999999]
    tags = ['F', 'E', 'C', 'B', 'A', 'S', 'Lenda']
    for i, v in enumerate(limites):
        if xp < v: return tags[i]
    return tags[-1]

class ContaUsuario:
    """Classe simples para simular autenticação do PROPRIETÁRIO."""
    def __init__(self, email, senha, cargo):
        self.email = email
        self.senha = senha
        self.cargo = cargo

PROPRIETARIO = ContaUsuario("caiquesanto674@gmail.com", SENHA_BASE, "PROPRIETÁRIO")

# 2. --- FEEDBACK EM COR (LOGS) ---
def frase_log(entidade, acao, sucesso=True, cor="\u001B[92m"):
    """Gera mensagens de log coloridas para melhor feedback."""
    status = "SUCESSO" if sucesso else "FALHA"
    nome = entidade.nome if hasattr(entidade, 'nome') else 'Sistema'
    cargo = entidade.cargo if hasattr(entidade, 'cargo') else 'Sistema'
    return f"{cor}[{nome}-{cargo}] {acao} - {status}\u001B[0m"

# 3. --- OBJETOS DO JOGO (RPG CORE) ---
class Personagem:
    """Representa uma Unidade, NPC ou Jogador (Base de RPG)."""
    def __init__(self, nome, cargo="Jogador", classe=None, raca=None):
        self.id = uuid.uuid4().hex
        self.nome = nome
        self.cargo = cargo
        self.raca = raca or random.choice(RACAS)
        self.classe = classe or random.choice(CLASSES)
        self.poderes = ProtocoloDePoder(cargo)
        # Bônus para PROPRIETÁRIO (Hierarquia e Poder)
        self.pv = 1200 if cargo == "PROPRIETÁRIO" else 100
        self.mana = 900 if cargo == "PROPRIETÁRIO" else 50
        self.xp = 0
        self.nivel = 1
        self.rank = 'F'
        self.ouro = random.randint(2000, 8000)
        self.arma = random.choice(ARMAS)
        self.vivo = True
        self.historico: List[str] = []

    def agir(self, acao: str, alvo=None):
        """Simula ações básicas de combate e exploração."""
        if acao == "atacar" and alvo:
            dano = random.randint(15, 40)
            alvo.pv = max(0, alvo.pv - dano)
            self.xp += 35
            msg = f"atacou {alvo.nome} tirou {dano} PV."
            return frase_log(self, msg, True)
        elif acao == "cura":
            self.pv = min(self.pv + 30, 120 + 10 * self.nivel) # Cura limitada ao PV máximo
            self.mana = max(0, self.mana - 10)
            return frase_log(self, "se curou 30 PV.")
        elif acao == "explorar":
            ganho = random.randint(10,80)
            self.ouro += ganho
            self.xp += 25
            return frase_log(self, f"explorou, ganhando {ganho} ouro.")
        return frase_log(self, f"ação {acao} executada (simulada)", True)

    def subir_nivel(self):
        """Lógica de progressão Isekai/RPG (a dificuldade aumenta exponencialmente)."""
        xp_necessario = 400 * (1.5 ** (self.nivel - 1))
        if self.xp >= xp_necessario:
            self.nivel += 1
            self.pv = int(self.pv * 1.2) # Aumento de 20% de PV por nível
            self.rank = rank_xp(self.xp)
            self.historico.append(f"Subiu para nível {self.nivel} (Patente {self.rank})")
            return frase_log(self, "subiu de nível! Poder Tático Aumentado!")
        return frase_log(self, f"XP insuficiente ({int(self.xp)}/{int(xp_necessario)})", False, "\u001B[91m")

    def ficha(self):
        """Retorna o resumo do personagem."""
        return {
            "Nome": self.nome, "Cargo": self.cargo, "Raça": self.raca, "Classe": self.classe,
            "PV": self.pv, "XP": self.xp, "Ouro": self.ouro,
            "Patente": self.rank, "Nível": self.nivel
        }

# 4. --- MÓDULO DE COMANDO E PROTOCOLO (Confirmação Militar) ---
class ProtocoloDeComando:
    """Gerencia a confirmação de operações críticas (Hierarquia e Segurança)."""

    @staticmethod
    def gerar_codigo_confirmacao(acao_chave: str, nivel_tecnologico: int, cargo_emissor: str, status_comportamento: str) -> str:
        """
        Gera o Código de Confirmação, agora incluindo o status de comportamento para maior segurança.
        """
        complexidade = nivel_tecnologico * 10 + CARGOS.index(cargo_emissor)
        semente = f"{acao_chave}:{SENHA_BASE}:{complexidade}:{status_comportamento}"
        codigo = hashlib.sha256(semente.encode()).hexdigest()[:6].upper()
        return codigo

    def validar_operacao_militar(self, emissor: Personagem, acao: str, codigo_inserido: str, base_militar: 'BaseMilitar') -> bool:
        """Valida e executa a operação militar, agora com simulação de resultado baseada no comportamento."""
        if acao not in ACOES_MILITARES:
            print(frase_log(base_militar, f"Ação {acao} não é militar crítica.", False))
            return False

        custo_eter = ACOES_MILITARES[acao]["consumo_eter"]
        if base_militar.recursos["Éter"] < custo_eter:
            print(frase_log(base_militar, f"Recursos Éter insuficientes ({custo_eter}) para {acao}.", False, "\u001B[91m"))
            return False

        nivel_tec = base_militar.sistema_tec.nivel
        codigo_esperado = self.gerar_codigo_confirmacao(acao, nivel_tec, emissor.cargo, base_militar.status_comportamento)

        if emissor.cargo == 'PROPRIETÁRIO' or codigo_inserido == codigo_esperado:
            base_militar.recursos["Éter"] -= custo_eter
            emissor.xp += ACOES_MILITARES[acao]["recompensa_xp"]

            # Simulação do resultado da operação
            modificador = COMPORTAMENTO_STATUS[base_militar.status_comportamento]
            fator_risco = modificador.get("risco", 0.5)

            if random.random() > fator_risco:
                base_militar.forca_belica += 200
                print(frase_log(emissor, f"Operação '{acao}' bem-sucedida! Força bélica aumentada.", True, "\u001B[96m"))
            else:
                base_militar.forca_belica -= 50
                print(frase_log(emissor, f"Operação '{acao}' teve perdas. Força bélica reduzida.", False, "\u001B[91m"))

            print(f"  > Nova Força Bélica da Base '{base_militar.nome}': {base_militar.forca_belica}")
            return True
        else:
            print(f"\u001B[91m[PROTOCOLO NEGADO] Código Inválido. Nível Tec: {nivel_tec}. (Esperado: {codigo_esperado})\u001B[0m")
            return False

# 5. --- ESTRUTURAS DO JOGO: ECONOMIA, TECNOLOGIA, REDE E BASE ---
class Economia:
    """Gerencia o mercado. Preços flutuam com base no Nível Tecnológico."""
    def __init__(self, tec: 'Tecnologia'):
        self.mercado = {"Ouro": 40000, "Éter": 1200, "Cristal": 300}
        self.tec = tec
        self.flutuacao = 1.0

    def atualizar_flutuacao(self):
        """A tecnologia estabiliza/impulsiona a economia (simulação de Sandbox/Tycoon)."""
        mod_tecnologia = 1 + (self.tec.nivel / 20)
        self.flutuacao = random.uniform(0.9, 1.1) * mod_tecnologia

    def transacao(self, recurso, qtd, jogador: Personagem):
        """Executa a compra de recursos."""
        self.atualizar_flutuacao()
        if qtd <= 0: return frase_log(jogador, "Qtd inválida", False)

        preco_base = self.mercado.get(recurso, 100) / 10
        preco_final = int(preco_base * self.flutuacao)
        total = preco_final * qtd

        if jogador.ouro >= total:
            jogador.ouro -= total
            self.mercado[recurso] -= qtd
            txt = f"comprou {qtd} de {recurso} por {total} Ouro. Preço/Un: {preco_final}"
            return frase_log(jogador, txt)
        return frase_log(jogador, "Ouro insuficiente", False, "\u001B[91m")

class Tecnologia:
    """Gerencia a progressão tecnológica (Análise e Teste)."""
    def __init__(self):
        self.nivel = 1
        self.inovacoes: List[str] = []

    def pesquisar(self, tecnologia: str, custo_eter: int, jogador: Personagem, base_militar: 'BaseMilitar'):
        """Avança o Nível Tecnológico com custo e concede bônus de poder."""
        if base_militar.recursos["Éter"] >= custo_eter:
            base_militar.recursos["Éter"] -= custo_eter
            self.nivel += 1
            self.inovacoes.append(tecnologia)
            base_militar.rede.atualizar_rede(self.nivel) # Atualiza a rede

            if tecnologia == 'IA Defensiva Quântica':
                jogador.pv += 500 # Aumento de poder tático do comandante
                print(frase_log(jogador, f"Tecnologia {tecnologia} desbloqueada! Comandante PV +500", True, "\u001B[93m"))
            return frase_log(jogador, f"Tecnologia {tecnologia} desbloqueada (Nível {self.nivel})!", True, "\u001B[93m")
        return frase_log(jogador, f"Éter insuficiente (custo: {custo_eter})", False, "\u001B[91m")

class RedeUniversal:
    """Simula a conectividade e segurança da base (Análise e Teste)."""
    def __init__(self, nome_base):
        self.nome = f"Rede Tática {nome_base}"
        self.status_rede: str = "Conectado"
        self.satelites_ativos: int = 5

    def atualizar_rede(self, nivel_tecnologico: int):
        """A segurança e estabilidade da rede dependem diretamente da Tecnologia."""
        if nivel_tecnologico >= 5:
            self.status_rede = "Conectado e Criptografado (Nível S)"
        elif nivel_tecnologico >= 3:
            self.status_rede = "Conectado e Estável (Nível B)"
        else:
            self.status_rede = "Vulnerável (Nível F)"

        self.satelites_ativos = 3 + (nivel_tecnologico * 2)
        print(frase_log(self, f"Rede atualizada. Status: {self.status_rede}", True, "\u001B[94m"))

class BaseMilitar:
    """O Hub central do jogo (Tycoon/Gerenciamento)."""
    def __init__(self, nome, comandante, sistema_eco, sistema_tec):
        self.nome = nome
        self.comandante = comandante
        self.recursos = {"Ouro": random.randint(12000, 40000), "Éter": random.randint(200, 800)}
        self.sistema_eco: Economia = sistema_eco
        self.sistema_tec: Tecnologia = sistema_tec
        self.rede = RedeUniversal(self.nome)
        self.status_comportamento: str = "NEUTRO"
        self.forca_belica: int = 1000

    def alterar_comportamento(self, novo_status: str):
        """Altera o comportamento da base (AGRESSIVO/DEFENSIVO/NEUTRO)."""
        if novo_status in COMPORTAMENTO_STATUS:
            self.status_comportamento = novo_status
            print(frase_log(self, f"Comportamento alterado para: {self.status_comportamento}", cor="\u001B[93m"))
            return True
        print(frase_log(self, f"Status '{novo_status}' inválido.", sucesso=False, cor="\u001B[91m"))
        return False

    def status(self):
        """Retorna o status detalhado da Base."""
        return {
            "Base": self.nome, "Comandante": self.comandante.nome,
            "Recursos": self.recursos, "Nível Tecnológico": self.sistema_tec.nivel,
            "Status da Rede": self.rede.status_rede
        }

# 6. --- IA ANALYTICS & NPC (Utility IA) ---
class IA_NPC:
    """IA de suporte e análise, usando Utility Scoring para decisões táticas."""
    def __init__(self, nome='IA Suprema'):
        self.nome = nome

    @staticmethod
    def _funcao_sigmoid(x: float, k: float = 8.0, x0: float = 0.5) -> float:
        """Função Sigmoid para transformar considerações em pontuações de utilidade."""
        return 1 / (1 + math.exp(-k * (x - x0)))

    @staticmethod
    def _pontuacao_utilidade(personagem: Personagem, alvo: Personagem) -> Dict[str, float]:
        """Calcula a utilidade de cada ação para o NPC usando uma curva sigmoid para a saúde."""
        pv_max_estimado_npc = 100 + 10 * personagem.nivel
        taxa_saude_npc = personagem.pv / pv_max_estimado_npc

        pv_max_estimado_alvo = 100 + 10 * alvo.nivel
        taxa_saude_alvo = alvo.pv / pv_max_estimado_alvo

        # Pontuação de saúde do NPC (0=morto, 1=saudável). Sigmoid faz a pontuação cair drasticamente abaixo de 50%
        pontuacao_saude_npc = IA_NPC._funcao_sigmoid(taxa_saude_npc)

        # Pontuação para ATACAR: útil se o NPC está saudável E o alvo está ferido.
        pontuacao_atacar = pontuacao_saude_npc * 0.6 + (1 - taxa_saude_alvo) * 0.4

        # Pontuação para CURAR: útil se o NPC está ferido (inverso da pontuação de saúde).
        pontuacao_curar = 1 - pontuacao_saude_npc

        # Pontuação para EXPLORAR: útil se o NPC está com saúde razoável e não houver ameaça imediata.
        pontuacao_explorar = pontuacao_saude_npc * 0.5

        return {"atacar": pontuacao_atacar, "cura": pontuacao_curar, "explorar": pontuacao_explorar}

    def decidir_acao_npc(self, npc: Personagem, alvo: Personagem) -> str:
        """Decide a ação de maior utilidade com base nos scores."""
        scores = self._pontuacao_utilidade(npc, alvo)

        # Regras de Ponderação
        if scores["cura"] > 0.6: return "cura" # Prioridade alta para cura se saúde < ~40%
        if scores["atacar"] > 0.7: return "atacar" # Ataca se a vantagem for clara

        # Escolhe a melhor ação restante ou explora por padrão
        del scores["cura"] # Já foi avaliada
        return max(scores, key=scores.get) if scores else "explorar"

    def analisar(self, personagem: Personagem) -> Dict[str, Any]:
        """Gera uma análise completa do perfil do personagem (Análise e Teste)."""
        perfil = "Agressivo" if personagem.xp > 500 else "Neutro"
        return {"Nome": personagem.nome,"Cargo": personagem.cargo,"Perfil": perfil,
                "Raça/Classe": f"{personagem.raca} / {personagem.classe}",
                "Poder Tático (Hierarquia)": personagem.nivel * (1 + CARGOS.index(personagem.cargo)/5),
                "Patente de XP": personagem.rank}

# 7. --- TESTE E EXECUÇÃO SIMULADA ---
if __name__ == "__main__":

    print("==== SUPREMO RPG IA: INÍCIO DA EXECUÇÃO (DEMO CONCEITUAL) ====")

    # 1. SETUP INICIAL
    proprietario = Personagem("Caíque", cargo="PROPRIETÁRIO")
    tec = Tecnologia()
    eco = Economia(tec)
    protocolo = ProtocoloDeComando()
    storage = ServicoDeArmazenamento()
    base = BaseMilitar("Bastião da Verdade", proprietario, eco, tec)
    ia = IA_NPC()

    npc_diretor = Personagem("Maria", cargo="Diretor", classe="Comandante", raca="Androide")
    vilao_inimigo = Personagem("Ezren", classe="Assassino", raca="Demônio")

    # Simula logins para o protocolo de entropia
    storage.logins[proprietario.id] = datetime.now()
    storage.logins[npc_diretor.id] = datetime.now()
    agente_inativo = Personagem("Inativo", cargo="Jogador")
    storage.logins[agente_inativo.id] = datetime.now() - timedelta(days=31)

    print("\n--- STATUS DE HIERARQUIA E BASE ---")
    print(base.status())
    print(proprietario.ficha())

    # 2. CICLO TECNOLOGIA E COMPORTAMENTO
    print("\n--- CICLO: TECNOLOGIA E COMPORTAMENTO ---")
    tec.pesquisar("Nanobots de Reparo", 100, proprietario, base)
    base.alterar_comportamento("AGRESSIVO")

    # 3. CICLO PROTOCOLO MILITAR
    print("\n--- CICLO: PROTOCOLO MILITAR ---")
    acao_alvo = "ATAQUE_TOTAL"
    codigo_npc_correto = protocolo.gerar_codigo_confirmacao(acao_alvo, tec.nivel, npc_diretor.cargo, base.status_comportamento)
    print(f"\u001B[90m[DEPURAÇÃO] Código de Confirmação para '{acao_alvo}': {codigo_npc_correto}\u001B[0m")
    protocolo.validar_operacao_militar(npc_diretor, acao_alvo, codigo_npc_correto, base)

    # 4. CICLO DE SEGURANÇA (ENTROPIA)
    print("\n--- CICLO: SEGURANÇA E ENTROPIA ---")
    storage.executar_protocolo_de_entropia()

    # 5. TESTE DE DECISÃO DA IA
    print("\n--- ANÁLISE E DECISÃO DA IA (UTILITY SCORING) ---")
    print(ia.analisar(vilao_inimigo))

    vilao_inimigo.pv = 15 # Deixa o vilão fraco para a IA decidir
    decisao = ia.decidir_acao_npc(vilao_inimigo, proprietario) # IA decide a ação do vilão
    print(f"IA decide para {vilao_inimigo.nome} (PV 15): {decisao.upper()}")

    print("\n==== EXECUÇÃO SIMULADA FINALIZADA ====")
