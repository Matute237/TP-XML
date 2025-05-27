from dataclasses import dataclass

@dataclass(init=False, repr=True, eq=True)
class CategoriaCargo:
    nombre: str
    
    