from typing import Dict

class Archivos:
    def __init__(self, archivos: Dict[str, str]) -> None:
        self.archivos = archivos

    def estudiantes(self) -> list[str]:
        return list(self.archivos)
    

class Archivo:
    