from app import db
from app.models import TipoEspecialidad

class TipoEspecialidadRepository:
    @staticmethod
    def crear(tipoespecialidad):
        """
        Crea un nuevo tipo de especialidad en la base de datos.
        :param tipoespecialidad: Objeto TipoEspecialidad a crear.
        :return: Objeto TipoEspecialidad creado.
        """
        db.session.add(tipoespecialidad)
        db.session.commit()
        
    @staticmethod
    def buscar_por_id(id: int):
        """
        Busca un tipo de especialidad por su ID.
        :param id: ID del tipo de especialidad a buscar.
        :return: Objeto TipoEspecialidad encontrado o None si no se encuentra.
        """
        return db.session.query(TipoEspecialidad).filter_by(id=id).first()
    
    @staticmethod
    def buscar_todos():
        """
        Busca todos los tipos de especialidad en la base de datos.
        :return: Lista de objetos TipoEspecialidad.
        """
        return db.session.query(TipoEspecialidad).all()

    @staticmethod
    def actualizar(tipoespecialidad) -> TipoEspecialidad:
        """
        Actualiza un tipo de especialidad existente en la base de datos.
        :param tipoespecialidad: Objeto TipoEspecialidad con los nuevos datos.
        :return: Objeto TipoEspecialidad actualizado.
        """
        tipoespecialidad_existente = db.session.merge(tipoespecialidad)
        if not tipoespecialidad_existente:
            return None
        return tipoespecialidad_existente
    
    @staticmethod
    def borrar_por_id(id: int) -> TipoEspecialidad:
        tipoespecialidad = db.session.query(TipoEspecialidad).filter_by(id=id).first()
        if not tipoespecialidad:
            return None
        db.session.delete(tipoespecialidad)
        db.session.commit()
        return tipoespecialidad