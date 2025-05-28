from app import db
from app.models import Alumno

class AlumnoRepository:
    @staticmethod
    def crear(alumno):
        db.session.add(alumno)
        db.session.commit()

    @staticmethod
    def buscar_por_id(id: int):
        return db.session.query(Alumno).filter_by(id=id).first()
    
    @staticmethod
    def buscar_todos():
        return db.session.query(Alumno).all()
    
    @staticmethod
    def actualizar(alumno) -> Alumno:
        alumno_existente = db.session.merge(alumno)
        if not alumno_existente:
            return None
        return alumno_existente
    
    @staticmethod
    def borrar_por_id(id: int) -> Alumno:
        alumno = db.session.query(Alumno).filter_by(id=id).first()
        if not alumno:
            return None
        db.session.delete(alumno)
        db.session.commit()
        return alumno