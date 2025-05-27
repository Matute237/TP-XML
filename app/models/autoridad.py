from dataclasses import dataclass
from app.models.cargo import Cargo

@dataclass(init=False, repr=True, eq=True)
class Autoridad():
    nombre: str
    cargo: Cargo
    telefono: str
    email: str
