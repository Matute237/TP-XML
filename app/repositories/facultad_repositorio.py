from app import db
from app.models import Facultad

class FacultadRepository:
    """
    Clase de repositorio para la entidad Facultad.
    """
    @staticmethod
    def crear(facultad):
        """
        Crea una nueva facultad en la base de datos.
        :param facultad: Objeto Facultad a crear.
        :return: Objeto Facultad creado.
        """
        db.session.add(facultad)
        db.session.commit()
        
    @staticmethod
    def buscar_por_id(id: int):
        """
        Busca una facultad por su ID.
        :param id: ID de la facultad a buscar.
        :return: Objeto Facultad encontrado o None si no se encuentra.
        """
        return db.session.query(Facultad).filter_by(id=id).first()
    
    @staticmethod
    def buscar_todos():
        """
        Busca todas las facultades en la base de datos.
        :return: Lista de objetos Facultad.
        """
        return db.session.query(Facultad).all()
    
    @staticmethod
    def actualizar_facultad(facultad) -> Facultad:
        """
        Actualiza una facultad existente en la base de datos.
        :param id: ID de la facultad a actualizar.
        :param facultad: Objeto Facultad con los nuevos datos.
        :return: Objeto Facultad actualizado.
        """
        facultad_existente = db.session.merge(facultad)
        if not facultad_existente:
            return None
        return facultad_existente
    
    @staticmethod
    def borrar_por_id(id: int) -> Facultad:
        """
        Borra una facultad por su ID.
        :param id: ID de la facultad a borrar.
        :return: Objeto Facultad borrado o None si no se encuentra.
        """
        facultad = db.session.query(Facultad).filter_by(id=id).first()
        if not facultad:
            return None
        db.session.delete(facultad)
        db.session.commit()
        return facultad
