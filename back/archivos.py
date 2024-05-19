from typing import Dict
from metrics import Metrics
from dup import code_tokens, parameterized_tokens, dup
from deltas import metrics_deltas

class Archivos:
    def __init__(self, archivos: Dict[str, str]) -> None:
        self.archivos = {matricula: Archivo(matricula, codigo) for matricula, codigo in archivos.items()}
        self.comparaciones = dict()
        self.heatmap = dict()

        for matricula1, archivo1 in self.archivos.items():
            for matricula2, archivo2 in self.archivos.items():
                comparacion_ = comparar_archivos(archivo1, archivo2)
                self.comparaciones[matricula1][matricula2] = comparacion_
                self.heatmap[matricula1][matricula2] = comparacion_['similitud']

    def estudiantes(self) -> list[str]:
        return [matricula for matricula in self.archivos]

    def comparacion(self, id_1: str, id_2: str):
        return self.comparaciones[id_1, id_2]

class Archivo:
    def __init__(self, id: str, code: str) -> None:
        self.id = id
        self.code = code
        self.metrics = Metrics(code)
        self.tokens = code_tokens(code)
        self.parameterized_tokens = parameterized_tokens(self.tokens)

    def __repr__(self) -> str:
        return f"Archivo({self.id}, {self.code})"
    
def comparar_archivos(archivo1: Archivo, archivo2: Archivo):
    codigo1, codigo2, block_ratio = dup(archivo1, archivo2)
    deltas, deltas_clasificacion, deltas_ratio = metrics_deltas(archivo1.metrics, archivo2.metrics)

    return {
        "codigo": {
            archivo1.id: codigo1,
            archivo2.id: codigo2,
            "similitud": block_ratio
        },
        "metricas": {
            "deltas": deltas,
            "clasificacion": deltas_clasificacion,
            "similitud": deltas_ratio
        },
        "similitud": (block_ratio * 0.6) + (deltas_ratio * 0.4)
    }