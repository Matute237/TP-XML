from dataclasses import dataclass
from app import db

@dataclass(init=False, repr=True, eq=True)
class EspecialidadModel(db.Model):
    __tablename__ = 'especialidades'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    especialidad = db.Column(db.Integer, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    letra = db.Column(db.String(1), nullable=True)
    observacion = db.Column(db.String(255), nullable=True)