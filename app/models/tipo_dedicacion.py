from dataclasses import dataclass

@dataclass(init=False, repr=True, eq=True)
class TipoDedicacion:
    nombre: str
    observacion: str
    
    