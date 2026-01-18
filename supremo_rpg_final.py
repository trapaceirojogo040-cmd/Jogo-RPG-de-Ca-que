# Arquivo Conceito: Supremo RPG AI X Final - Versão PT-BR
# Arquitetura Unificada de RPG de Estratégia, Hierarquia, Economia e Protocolo de IA.
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
        self.nivel_volicao: int = random.randint(50, 100)
        self.sinergia_moral: float = 1.0
        self.habilidades = self._definir_habilidades(cargo)

    def _definir_habilidades(self, cargo: str) -> Dict[str, str]:
        if "PROPRIETARIO" in cargo or "Comandante" in cargo:
            self.nivel_volicao = 999
            self.sinergia_moral = 1.5
            return {
                "Poder Psicológico": "Volição (Controle de Causalidade Avançado)",
                "Força Bélica": "Arsenal de Éter e Defesa Quântica",
            }
        return {"Poder Psicológico": "Padrão", "Força Bélica": "Básico"}

class ServicoDeArmazenamento:
    """Gerencia o armazenamento seguro e o protocolo de destruição de dados."""
    def __init__(self):
        self.registros_login: Dict[str, datetime] = {}

    def executar_protocolo_entropia(self, max_dias_inativo: int = 30):
        """Executa a Lei da Destruição de Dados (Entropia)."""
        data_corte = datetime.now() - timedelta(days=max_dias_inativo)
        chaves_para_destruir = [
            id_usuario for id_usuario, ultimo_login in self.registros_login.items()
            if ultimo_login < data_corte
        ]
        for id_usuario in chaves_para_destruir:
            del self.registros_login[id_usuario]
            print(f" [PROTOCOLO DE ENTROPIA]: Dados de {id_usuario[:8]} destruídos por inatividade.")

# 2. --- CONFIGURAÇÃO GLOBAL E HIERARQUIA ---
CLASSES = ['Guerreiro', 'Mago', 'Comandante', 'Engenheiro', 'Assassino', 'Espadachim', 'Clérigo']
RACAS = ['Humano', 'Elfo', 'Orc', 'Demônio', 'Androide', 'IA']
ARMAS = ['Espada Laser', 'Fuzil de Plasma', 'Varinha Arcana', 'Canhão Orbital']
TECNOLOGIAS = ['Campo de Força Quântico', 'Nanobots de Reparo', 'Bombardeio Orbital', 'Teleportador Tático', 'IA Defensiva']
CARGOS = ['PROPRIETARIO', 'Administrador', 'Diretor', 'Mestre Mor', 'Mestre de Jogo', 'Moderador', 'Jogador']

# Definições de Comportamento Militar
FRASES_MILITARES: Dict[str, str] = {
    "ATAQUE_TOTAL": "O preço da vitória é a preparação",
    "RECUO_ESTRATEGICO": "Reagrupar é prioridade, a força retornará",
    "DEFESA_IMEDIATA": "Linhas de defesa ativas, posição mantida",
}
STATUS_COMPORTAMENTO: Dict[str, Dict[str, Any]] = {
    "AGRESSIVO": {"risco": 0.8, "consumo_recursos": 1.5, "bonus_dano": 0.2},
    "DEFENSIVO": {"risco": 0.2, "consumo_recursos": 0.5, "bonus_defesa": 0.3},
    "NEUTRO": {"risco": 0.5, "consumo_recursos": 1.0},
}

# Ações Militares que requerem Protocolo de Confirmação
ACOES_MILITARES = {
    "ASSALTO_FINAL": {"risco": 0.9, "consumo_eter": 50, "recompensa_xp": 500},
    "REAGRUPAMENTO": {"risco": 0.1, "consumo_eter": 10, "recompensa_xp": 50},
    "DESCOBERTA_PLANETA": {"risco": 0.5, "consumo_eter": 30, "recompensa_xp": 250},
    "ATAQUE_TOTAL": {"risco": 0.8, "consumo_eter": 40, "recompensa_xp": 400}
}
SENHA_MESTRA = "edson4020SS" # Base para geração do código de confirmação

def calcular_patente_xp(xp):
    """Calcula a Patente de poder (F, E, C, B, A, S, Lendário) baseado na XP total."""
    limites = [100, 500, 2500, 8000, 30000, 70000, 99999999]
    patentes = ['F', 'E', 'C', 'B', 'A', 'S', 'Lendário']
    for i, v in enumerate(limites):
        if xp < v: return patentes[i]
    return patentes[-1]

class ContaUsuario:
    """Classe simples para simular autenticação do PROPRIETARIO."""
    def __init__(self, email, senha, cargo):
        self.email = email
        self.senha = senha
        self.cargo = cargo

PROPRIETARIO_CONTA = ContaUsuario("caiquesanto674@gmail.com", SENHA_MESTRA, "PROPRIETARIO")

# 2. --- FEEDBACK EM COR (LOGS) ---
def criar_log(entidade, acao, sucesso=True, cor="\u001B[92m"):
    """Gera mensagens de log coloridas para melhor feedback visual."""
    status = "SUCESSO" if sucesso else "FALHA"
    nome = entidade.nome if hasattr(entidade, 'nome') else 'Sistema'
    cargo = entidade.cargo if hasattr(entidade, 'cargo') else 'Sistema'
    return f"{cor}[{nome}-{cargo}] {acao} - {status}\u001B[0m"

# 3. --- OBJETOS DO JOGO (NÚCLEO RPG) ---
class Jogador:
    """Representa uma Unidade, NPC ou Jogador (Base de RPG)."""
    def __init__(self, nome, cargo="Jogador", classe=None, raca=None):
        self.id = uuid.uuid4().hex
        self.nome = nome
        self.cargo = cargo
        self.raca = raca or random.choice(RACAS)
        self.classe = classe or random.choice(CLASSES)
        self.poderes = ProtocoloDePoder(cargo)
        # Bônus para PROPRIETARIO (Hierarquia e Poder)
        self.pontos_vida = 1200 if cargo == "PROPRIETARIO" else 100
        self.mana = 900 if cargo == "PROPRIETARIO" else 50
        self.xp = 0
        self.nivel = 1
        self.patente = 'F'
        self.ouro = random.randint(2000, 8000)
        self.arma = random.choice(ARMAS)
        self.esta_vivo = True
        self.historico: List[str] = []

    def executar_acao(self, acao: str, alvo=None):
        """Simula ações básicas de combate e exploração."""
        if acao == "atacar" and alvo:
            dano = random.randint(15, 40)
            alvo.pontos_vida = max(0, alvo.pontos_vida - dano)
            self.xp += 35
            msg = f"atacou {alvo.nome} e causou {dano} de dano."
            return criar_log(self, msg, True)
        elif acao == "curar":
            self.pontos_vida = min(self.pontos_vida + 30, 120 + 10 * self.nivel) # Cura limitada ao PV máximo
            self.mana = max(0, self.mana - 10)
            return criar_log(self, "curou 30 pontos de vida.")
        elif acao == "explorar":
            ganho_ouro = random.randint(10,80)
            self.ouro += ganho_ouro
            self.xp += 25
            return criar_log(self, f"explorou e ganhou {ganho_ouro} de ouro.")
        return criar_log(self, f"ação '{acao}' executada (simulada)", True)

    def subir_de_nivel(self):
        """Lógica de progressão de nível (a dificuldade aumenta exponencialmente)."""
        xp_necessario = 400 * (1.5 ** (self.nivel - 1))
        if self.xp >= xp_necessario:
            self.nivel += 1
            self.pontos_vida = int(self.pontos_vida * 1.2) # Aumento de 20% de PV por nível
            self.patente = calcular_patente_xp(self.xp)
            self.historico.append(f"Avançou para o nível {self.nivel} (Patente {self.patente})")
            return criar_log(self, "subiu de nível! Poder Tático Aumentado!")
        return criar_log(self, f"XP insuficiente ({int(self.xp)}/{int(xp_necessario)})", False, "\u001B[91m")

    def mostrar_ficha(self):
        """Retorna um resumo dos atributos do jogador."""
        return {
            "Nome": self.nome, "Cargo": self.cargo, "Raça": self.raca, "Classe": self.classe,
            "PV": self.pontos_vida, "XP": self.xp, "Ouro": self.ouro,
            "Patente": self.patente, "Nível": self.nivel
        }

# 4. --- MÓDULO DE COMANDO E PROTOCOLO (Confirmação Militar) ---
class ProtocoloDeConfirmacao:
    """Gerencia a confirmação de operações críticas, garantindo hierarquia e segurança."""

    @staticmethod
    def gerar_codigo_confirmacao(chave_acao: str, nivel_tecnologico: int, cargo_emissor: str, status_comportamento: str) -> str:
        """
        Gera um Código de Confirmação seguro para operações militares.

        O código é baseado em uma combinação de fatores: a ação a ser executada, o nível
        tecnológico da base, o cargo do emissor e o comportamento militar atual.

        Returns:
            str: Um código de confirmação de 6 caracteres.
        """
        # A complexidade aumenta com o nível tecnológico e a posição hierárquica
        complexidade = nivel_tecnologico * 10 + CARGOS.index(cargo_emissor)
        semente = f"{chave_acao}:{SENHA_MESTRA}:{complexidade}:{status_comportamento}"
        codigo = hashlib.sha256(semente.encode()).hexdigest()[:6].upper()
        return codigo

    def validar_codigo(self, chave_acao: str, nivel_tecnologico: int, cargo_emissor: str, status_comportamento: str, codigo_fornecido: str) -> bool:
        """
        Valida se um código fornecido corresponde ao código esperado.

        Returns:
            bool: True se o código for válido, False caso contrário.
        """
        codigo_esperado = self.gerar_codigo_confirmacao(chave_acao, nivel_tecnologico, cargo_emissor, status_comportamento)
        if codigo_fornecido == codigo_esperado:
            return True
        else:
            print(f"\u001B[91m[PROTOCOLO NEGADO] Código Inválido. Nível Tec: {nivel_tecnologico}. (Esperado: {codigo_esperado})\u001B[0m")
            return False

    def validar_operacao_militar(self, emissor: Jogador, acao: str, codigo_fornecido: str, base_militar: 'BaseMilitar') -> bool:
        """Valida e executa uma operação militar, consumindo recursos e aplicando resultados."""
        if acao not in ACOES_MILITARES:
            print(criar_log(base_militar, f"Ação '{acao}' não é uma operação militar crítica.", False))
            return False

        custo_eter = ACOES_MILITARES[acao]["consumo_eter"]
        if base_militar.recursos["Éter"] < custo_eter:
            print(criar_log(base_militar, f"Recursos de Éter insuficientes ({custo_eter}) para {acao}.", False, "\u001B[91m"))
            return False

        # O PROPRIETARIO tem autoridade para ignorar a validação de código
        if emissor.cargo == 'PROPRIETARIO':
            is_valido = True
        else:
            is_valido = self.validar_codigo(
                chave_acao=acao,
                nivel_tecnologico=base_militar.sistema_tecnologico.nivel,
                cargo_emissor=emissor.cargo,
                status_comportamento=base_militar.status_comportamento,
                codigo_fornecido=codigo_fornecido
            )

        if is_valido:
            base_militar.recursos["Éter"] -= custo_eter
            emissor.xp += ACOES_MILITARES[acao]["recompensa_xp"]

            modificador_comportamento = STATUS_COMPORTAMENTO[base_militar.status_comportamento]
            fator_risco = modificador_comportamento.get("risco", 0.5)

            if random.random() > fator_risco:
                base_militar.forca_belica += 200
                print(criar_log(emissor, f"Operação '{acao}' bem-sucedida! Força bélica aumentada.", True, "\u001B[96m"))
            else:
                base_militar.forca_belica -= 50
                print(criar_log(emissor, f"Operação '{acao}' resultou em perdas. Força bélica reduzida.", False, "\u001B[91m"))

            print(f"  > Nova Força Bélica da Base '{base_militar.nome}': {base_militar.forca_belica}")
            return True

        return False

# 5. --- ESTRUTURAS DO JOGO: ECONOMIA, TECNOLOGIA, REDE E BASE ---
class Economia:
    """Gerencia o mercado. Preços flutuam com base no Nível Tecnológico."""
    def __init__(self, tecnologia: 'Tecnologia'):
        self.mercado = {"Ouro": 40000, "Éter": 1200, "Cristal": 300}
        self.tecnologia = tecnologia
        self.flutuacao = 1.0

    def atualizar_flutuacao(self):
        """A tecnologia estabiliza e impulsiona a economia."""
        modificador_tecnologia = 1 + (self.tecnologia.nivel / 20)
        self.flutuacao = random.uniform(0.9, 1.1) * modificador_tecnologia

    def realizar_transacao(self, recurso: str, quantidade: int, jogador: Jogador):
        """Executa a compra de recursos por um jogador."""
        self.atualizar_flutuacao()
        if quantidade <= 0: return criar_log(jogador, "Quantidade inválida para transação.", False)

        preco_base = self.mercado.get(recurso, 100) / 10
        preco_final = int(preco_base * self.flutuacao)
        custo_total = preco_final * quantidade

        if jogador.ouro >= custo_total:
            jogador.ouro -= custo_total
            self.mercado[recurso] -= quantidade
            msg = f"comprou {quantidade} de {recurso} por {custo_total} Ouro. Preço/Un: {preco_final}"
            return criar_log(jogador, msg)
        return criar_log(jogador, "Ouro insuficiente para a compra.", False, "\u001B[91m")

class Tecnologia:
    """Gerencia a progressão tecnológica da base."""
    def __init__(self):
        self.nivel = 1
        self.inovacoes: List[str] = []

    def pesquisar_tecnologia(self, nome_tecnologia: str, custo_eter: int, jogador: Jogador, base_militar: 'BaseMilitar'):
        """Avança o Nível Tecnológico e concede bônus de poder."""
        if base_militar.recursos["Éter"] >= custo_eter:
            base_militar.recursos["Éter"] -= custo_eter
            self.nivel += 1
            self.inovacoes.append(nome_tecnologia)
            base_militar.rede.atualizar_rede(self.nivel)

            if nome_tecnologia == 'IA Defensiva Quântica':
                jogador.pontos_vida += 500
                print(criar_log(jogador, f"Tecnologia '{nome_tecnologia}' desbloqueada! Comandante PV +500", True, "\u001B[93m"))
            return criar_log(jogador, f"Tecnologia '{nome_tecnologia}' desbloqueada (Nível {self.nivel})!", True, "\u001B[93m")
        return criar_log(jogador, f"Éter insuficiente para pesquisa (custo: {custo_eter})", False, "\u001B[91m")

class RedeUniversal:
    """Simula a conectividade e segurança da base."""
    def __init__(self, nome_base):
        self.nome = f"Rede Tática {nome_base}"
        self.status_rede: str = "Conectado"
        self.satelites_ativos: int = 5

    def atualizar_rede(self, nivel_tecnologico: int):
        """A segurança da rede depende diretamente do nível tecnológico."""
        if nivel_tecnologico >= 5:
            self.status_rede = "Conectado e Criptografado (Nível S)"
        elif nivel_tecnologico >= 3:
            self.status_rede = "Conectado e Estável (Nível B)"
        else:
            self.status_rede = "Vulnerável (Nível F)"

        self.satelites_ativos = 3 + (nivel_tecnologico * 2)
        print(criar_log(self, f"Rede atualizada. Status: {self.status_rede}", True, "\u001B[94m"))

class BaseMilitar:
    """O Hub central de gerenciamento do jogo."""
    def __init__(self, nome, comandante, sistema_economico, sistema_tecnologico):
        self.nome = nome
        self.comandante = comandante
        self.recursos = {"Ouro": random.randint(12000, 40000), "Éter": random.randint(200, 800)}
        self.sistema_economico: Economia = sistema_economico
        self.sistema_tecnologico: Tecnologia = sistema_tecnologico
        self.rede = RedeUniversal(self.nome)
        self.status_comportamento: str = "NEUTRO"
        self.forca_belica: int = 1000

    def alterar_comportamento_base(self, novo_status: str):
        """Altera o comportamento estratégico da base (AGRESSIVO/DEFENSIVO/NEUTRO)."""
        if novo_status in STATUS_COMPORTAMENTO:
            self.status_comportamento = novo_status
            print(criar_log(self, f"Comportamento alterado para: {self.status_comportamento}", cor="\u001B[93m"))
            return True
        print(criar_log(self, f"Status de comportamento '{novo_status}' inválido.", sucesso=False, cor="\u001B[91m"))
        return False

    def mostrar_status(self):
        """Retorna um dicionário com o status detalhado da Base."""
        return {
            "Base": self.nome, "Comandante": self.comandante.nome,
            "Recursos": self.recursos, "Nível Tecnológico": self.sistema_tecnologico.nivel,
            "Status da Rede": self.rede.status_rede
        }

# 6. --- ANÁLISE DE IA E COMPORTAMENTO DE NPC (Utility AI) ---
class IA_NPC:
    """IA de suporte que usa Utility Scoring para tomar decisões táticas."""
    def __init__(self, nome='IA Suprema'):
        self.nome = nome

    @staticmethod
    def _funcao_sigmoide(x: float, k: float = 8.0, x0: float = 0.5) -> float:
        """Função Sigmoide para normalizar valores em uma pontuação de utilidade."""
        return 1 / (1 + math.exp(-k * (x - x0)))

    @staticmethod
    def _calcular_pontuacao_utilidade(personagem: Jogador, alvo: Jogador) -> Dict[str, float]:
        """Calcula a utilidade de cada ação para o NPC."""
        pv_max_estimado_npc = 100 + 10 * personagem.nivel
        taxa_saude_npc = personagem.pontos_vida / pv_max_estimado_npc

        pv_max_estimado_alvo = 100 + 10 * alvo.nivel
        taxa_saude_alvo = alvo.pontos_vida / pv_max_estimado_alvo

        pontuacao_saude_npc = IA_NPC._funcao_sigmoide(taxa_saude_npc)

        pontuacao_atacar = pontuacao_saude_npc * 0.6 + (1 - taxa_saude_alvo) * 0.4
        pontuacao_curar = 1 - pontuacao_saude_npc
        pontuacao_explorar = pontuacao_saude_npc * 0.5

        return {"atacar": pontuacao_atacar, "curar": pontuacao_curar, "explorar": pontuacao_explorar}

    def decidir_acao_npc(self, npc: Jogador, alvo: Jogador) -> str:
        """Decide a ação de maior utilidade com base nas pontuações."""
        pontuacoes = self._calcular_pontuacao_utilidade(npc, alvo)

        if pontuacoes["curar"] > 0.6: return "curar"
        if pontuacoes["atacar"] > 0.7: return "atacar"

        del pontuacoes["curar"]
        return max(pontuacoes, key=pontuacoes.get) if pontuacoes else "explorar"

    def analisar_perfil(self, jogador: Jogador) -> Dict[str, Any]:
        """Gera uma análise completa do perfil do jogador."""
        perfil = "Agressivo" if jogador.xp > 500 else "Neutro"
        return {"Nome": jogador.nome, "Cargo": jogador.cargo, "Perfil": perfil,
                "Raça/Classe": f"{jogador.raca} / {jogador.classe}",
                "Poder Tático (Hierarquia)": jogador.nivel * (1 + CARGOS.index(jogador.cargo)/5),
                "Patente de XP": jogador.patente}

# 7. --- TESTE E EXECUÇÃO DA SIMULAÇÃO ---
if __name__ == "__main__":

    print("==== SUPREMO RPG AI: INÍCIO DA SIMULAÇÃO (DEMO CONCEITUAL) ====")

    # 1. SETUP INICIAL
    jogador_proprietario = Jogador("Caíque", cargo="PROPRIETARIO")
    sistema_tecnologico = Tecnologia()
    sistema_economico = Economia(sistema_tecnologico)
    protocolo_confirmacao = ProtocoloDeConfirmacao()
    servico_armazenamento = ServicoDeArmazenamento()
    base_militar = BaseMilitar("Bastião da Verdade", jogador_proprietario, sistema_economico, sistema_tecnologico)
    ia_npc = IA_NPC()

    npc_diretor = Jogador("Maria", cargo="Diretor", classe="Comandante", raca="Androide")
    vilao_inimigo = Jogador("Ezren", classe="Assassino", raca="Demônio")

    # Simula logins para o protocolo de entropia
    servico_armazenamento.registros_login[jogador_proprietario.id] = datetime.now()
    servico_armazenamento.registros_login[npc_diretor.id] = datetime.now()
    agente_inativo = Jogador("Inativo", cargo="Jogador")
    servico_armazenamento.registros_login[agente_inativo.id] = datetime.now() - timedelta(days=31)

    print("\n--- STATUS DE HIERARQUIA E BASE ---")
    print(base_militar.mostrar_status())
    print(jogador_proprietario.mostrar_ficha())

    # 2. CICLO DE TECNOLOGIA E COMPORTAMENTO
    print("\n--- CICLO: TECNOLOGIA E COMPORTAMENTO ---")
    sistema_tecnologico.pesquisar_tecnologia("Nanobots de Reparo", 100, jogador_proprietario, base_militar)
    base_militar.alterar_comportamento_base("AGRESSIVO")

    # 3. CICLO DE PROTOCOLO MILITAR
    print("\n--- CICLO: PROTOCOLO MILITAR ---")
    acao_alvo = "ATAQUE_TOTAL"
    codigo_npc_correto = protocolo_confirmacao.gerar_codigo_confirmacao(acao_alvo, sistema_tecnologico.nivel, npc_diretor.cargo, base_militar.status_comportamento)
    print(f"\u001B[90m[DEPURAÇÃO] Código de Confirmação para '{acao_alvo}': {codigo_npc_correto}\u001B[0m")
    protocolo_confirmacao.validar_operacao_militar(npc_diretor, acao_alvo, codigo_npc_correto, base_militar)

    # 4. CICLO DE SEGURANÇA (ENTROPIA)
    print("\n--- CICLO: SEGURANÇA E ENTROPIA ---")
    servico_armazenamento.executar_protocolo_entropia()

    # 5. TESTE DE DECISÃO DA IA
    print("\n--- ANÁLISE E DECISÃO DA IA (UTILITY SCORING) ---")
    print(ia_npc.analisar_perfil(vilao_inimigo))

    vilao_inimigo.pontos_vida = 15 # Deixa o vilão fraco para a IA decidir
    decisao_ia = ia_npc.decidir_acao_npc(vilao_inimigo, jogador_proprietario)
    print(f"IA decide para {vilao_inimigo.nome} (PV: 15): {decisao_ia.upper()}")

    # 6. TESTE DE VALIDAÇÃO DE CÓDIGO
    print("\n--- CICLO: VALIDAÇÃO DE CÓDIGO DE CONFIRMAÇÃO ---")
    acao_teste = "ASSALTO_FINAL"
    codigo_correto_teste = protocolo_confirmacao.gerar_codigo_confirmacao(
        acao_teste, sistema_tecnologico.nivel, npc_diretor.cargo, base_militar.status_comportamento
    )
    codigo_incorreto_teste = "XXXXXX"

    print(f"Simulando validação para a ação '{acao_teste}' com código incorreto:")
    protocolo_confirmacao.validar_operacao_militar(npc_diretor, acao_teste, codigo_incorreto_teste, base_militar)

    print(f"\nSimulando validação para a ação '{acao_teste}' com código correto:")
    protocolo_confirmacao.validar_operacao_militar(npc_diretor, acao_teste, codigo_correto_teste, base_militar)


    print("\n==== SIMULAÇÃO FINALIZADA ====")
