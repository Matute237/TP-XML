from dataclasses import dataclass

@dataclass(init=False, repr=True, eq=True)
class Area():
    nombre: str
    
