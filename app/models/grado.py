from dataclasses import dataclass 
from app import db


@dataclass(init=False, repr=True, eq=True)
class Grado(db.Model):
    __tablename__ = 'grados'
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre: str = db.Column(db.String(50), nullable=True)
    descripcion: str = db.Column(db.String(200), nullable=True)
    


    