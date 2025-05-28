from dataclasses import dataclass

@dataclass(init=False, repr=True, eq=True)
class Materia():
    nombre: str
    codigo: str
    observacion: str