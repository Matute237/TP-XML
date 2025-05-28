from app import db
from app.models import Especialidad

class EspecialidadRepository:

    @staticmethod
    def crear(especialidad):
        db.session.add(especialidad)
        db.session.commit()

    @staticmethod
    def buscar_por_id(id: int):
        return db.session.query(Especialidad).filter_by(id=id).first()

    @staticmethod
    def buscar_todos():
        return db.session.query(Especialidad).all()

    @staticmethod
    def actualizar(especialidad) -> Especialidad:
        especialidad_existente = db.session.merge(especialidad)
        if not especialidad_existente:
            return None
        return especialidad_existente
    
    @staticmethod
    def borrar_por_id(id: int) -> Especialidad:
        especialidad = db.session.query(Especialidad).filter_by(id=id).first()
        if not especialidad:
            return None
        db.session.delete(especialidad)
        db.session.commit()
        return especialidad

