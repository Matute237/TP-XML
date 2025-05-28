from app import db
from app.models import Departamento

class DepartamentoRepository:

    @staticmethod
    def crear(departamento):
        """
        Crea un nuevo departamento en la base de datos.
        :param departamento: Objeto Departamento a crear.
        :return: Objeto Departamento creado.
        """
        db.session.add(departamento)
        db.session.commit()

    @staticmethod
    def buscar_por_id(id: int):
        """
        Busca un departamento por su ID.
        :param id: ID del departamento a buscar.
        :return: Objeto Departamento encontrado o None si no se encuentra.
        """
        return db.session.query(Departamento).filter_by(id=id).first()
    
    @staticmethod
    def buscar_todos():
        """
        Busca todos los departamentos en la base de datos.
        :return: Lista de objetos Departamento.
        """
        return db.session.query(Departamento).all()
    
    @staticmethod
    def actualizar(departamento) -> Departamento:
        """
        Actualiza un departamento existente en la base de datos.
        :param departamento: Objeto Departamento con los nuevos datos.
        :return: Objeto Departamento actualizado.
        """
        departamento_existente = db.session.merge(departamento)
        if not departamento_existente:
            return None
        return departamento_existente
    
    @staticmethod
    def borrar_por_id(id: int) -> Departamento:
        """
        Borra un departamento por su ID.
        :param id: ID del departamento a borrar.
        :return: Objeto Departamento borrado o None si no se encuentra.
        """
        departamento = db.session.query(Departamento).filter_by(id=id).first()
        if not departamento:
            return None
        db.session.delete(departamento)
        db.session.commit()
        return departamento