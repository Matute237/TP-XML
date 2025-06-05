from dataclasses import dataclass
from app import db

@dataclass(init=False, repr=True, eq=True)
class Materia(db.Model):
    __tablename__ = 'materias'
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)    
    especialidad = db.Column(db.Integer, nullable=True)
    plan = db.Column(db.Integer, nullable=True)
    materia = db.Column(db.String(50), nullable=True)
    nombre = db.Column(db.String(200), nullable=True)
    ano = db.Column(db.Integer, nullable=True)
