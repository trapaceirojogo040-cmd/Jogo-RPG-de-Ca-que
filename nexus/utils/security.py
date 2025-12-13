class Security:
    """Validação de inputs, arquivos e scripts."""
    @staticmethod
    def validate_path(path: str) -> bool:
        return ".." not in path
