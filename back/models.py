from typing import Dict, Any

class Archivos:
    def __init__(self, archivos: Dict[str, str]) -> None:
        self.archivos = archivos

    def estudiantes(self) -> list[str]:
        return list(self.archivos)
    
class Token:
    """
    Representacion simplificada de `lexer.Token` que solo guarda su tipo y valor para eliminar ruido
    """
    def __init__(self, kind: str, value: Any) -> None:
        self.kind = kind
        self.value = value

    def __repr__(self) -> str:
        return f"Token(kind={self.kind}, value={self.value})"