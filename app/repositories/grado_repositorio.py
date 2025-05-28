from app import db
from app.models import Grado

class GradoRepository:
    @staticmethod
    def crear(grado):
        """
        Crea un nuevo grado en la base de datos.
        :param grado: Objeto Grado a crear.
        :return: Objeto Grado creado.
        """
        db.session.add(grado)
        db.session.commit()
        
    @staticmethod
    def buscar_por_id(id: int):
        """
        Busca un grado por su ID.
        :param id: ID del grado a buscar.
        :return: Objeto Grado encontrado o None si no se encuentra.
        """
        return db.session.query(Grado).filter_by(id=id).first()
    

    @staticmethod
    def buscar_todos():
        """
        Busca todos los grados en la base de datos.
        :return: Lista de objetos Grado.
        """
        return db.session.query(Grado).all()
    

    @staticmethod
    def actualizar_grado(grado) -> Grado:
        """
        Actualiza un grado en la base de datos.
        :param grado: Objeto Grado a actualizar.
        :return: Objeto Grado actualizado.
        """
        grado_existente = db.session.merge(grado)
        if not grado_existente:
            return None
        return grado_existente 
    
    @staticmethod
    def borrar_por_id(id: int) -> Grado:
        """
        Borra un grado por su ID.
        :param id: ID del grado a borrar.
        :return: Objeto Grado borrado o None si no se encuentra.
        """
        grado = db.session.query(Grado).filter_by(id=id).first()
        if not grado:
            return None
        db.session.delete(grado)
        db.session.commit()
        return grado