# -*- coding: utf-8 -*-
"""
Módulo de Backup (Cronos): Ferramenta para criar e restaurar
snapshots do estado atual do projeto.
"""
import os
import shutil
from datetime import datetime
from typing import List

class SistemaDeBackup:
    """
    Gerencia a criação e restauração de snapshots completos do projeto,
    garantindo que o progresso possa ser salvo e recuperado.
    """
    def __init__(self, root: str = ".", backup_root: str = ".apolo_backups"):
        """
        Args:
            root (str): O diretório raiz do projeto a ser "snapshotado".
            backup_root (str): O diretório onde os snapshots serão armazenados.
        """
        self.root = root
        self.backup_root = backup_root

        if not os.path.exists(self.backup_root):
            os.makedirs(self.backup_root)

    def criar_snapshot(self, sufixo: str = "") -> str:
        """
        Cria uma cópia de segurança completa do diretório raiz do projeto.

        Args:
            sufixo (str): Um sufixo opcional para adicionar ao nome do snapshot.

        Returns:
            str: O caminho para o snapshot recém-criado.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nome_snapshot = f"snapshot_{timestamp}{'_' + sufixo if sufixo else ''}"
        snapshot_path = os.path.join(self.backup_root, nome_snapshot)

        # Ignora o próprio diretório de backup e outros arquivos temporários
        ignore_patterns = shutil.ignore_patterns(
            os.path.basename(self.backup_root), '.__pycache__', '*.pyc', '.*', 'codigo_arquivado'
        )

        shutil.copytree(
            self.root,
            snapshot_path,
            dirs_exist_ok=True,
            ignore=ignore_patterns
        )
        print(f"Snapshot criado com sucesso em: {snapshot_path}")
        return snapshot_path

    def listar_snapshots(self) -> List[str]:
        """
        Lista todos os snapshots disponíveis no diretório de backup.

        Returns:
            List[str]: Uma lista ordenada dos nomes dos snapshots.
        """
        if not os.path.exists(self.backup_root):
            return []
        return sorted(os.listdir(self.backup_root))

    def restaurar_snapshot(self, nome_snapshot: str):
        """
        Restaura o projeto para o estado de um snapshot específico.
        AVISO: Isso sobrescreverá os arquivos atuais.

        Args:
            nome_snapshot (str): O nome do snapshot a ser restaurado.

        Raises:
            FileNotFoundError: Se o snapshot especificado não for encontrado.
        """
        snapshot_path = os.path.join(self.backup_root, nome_snapshot)
        if not os.path.exists(snapshot_path):
            raise FileNotFoundError(f"Snapshot '{nome_snapshot}' não encontrado em '{self.backup_root}'.")

        print(f"Restaurando snapshot '{nome_snapshot}'...")
        for item in os.listdir(snapshot_path):
            src = os.path.join(snapshot_path, item)
            dst = os.path.join(self.root, item)

            if os.path.isdir(src):
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
        print("Restauração concluída.")
