from app import db
from app.models import TipoDocumento

class TipoDocumentoRepository:

    @staticmethod
    def crear(tipodocumento):
        """
        Crea un nuevo tipo de documento en la base de datos.
        :param tipodocumento: Objeto TipoDocumento a crear.
        :return: Objeto TipoDocumento creado.
        """
        db.session.add(tipodocumento)
        db.session.commit()

    @staticmethod
    def buscar_por_id(id: int):
        """
        Busca un tipo de documento por su ID.
        :param id: ID del tipo de documento a buscar.
        :return: Objeto TipoDocumento encontrado o None si no se encuentra.
        """
        return db.session.query(TipoDocumento).filter_by(id=id).first()
    
    @staticmethod
    def buscar_todos():
        """
        Busca todos los tipos de documentos en la base de datos.
        :return: Lista de objetos TipoDocumento.
        """
        return db.session.query(TipoDocumento).all()
    
    @staticmethod
    def actualizar(tipodocumento) -> TipoDocumento:
        """
        Actualiza un tipo de documento existente en la base de datos.
        :param tipodocumento: Objeto TipoDocumento a actualizar.
        :return: Objeto TipoDocumento actualizado o None si no se encuentra.
        """
        tipodocumento_existente = db.session.merge(tipodocumento)
        if not tipodocumento_existente:
            return None
        return tipodocumento_existente
    
    @staticmethod
    def borrar_por_id(id: int) -> TipoDocumento:
        """
        Borra un tipo de documento por su ID.
        :param id: ID del tipo de documento a borrar.
        :return: True si se borra correctamente, False si no se encuentra.
        """
        tipodocumento = db.session.query(TipoDocumento).filter_by(id=id).first()
        if not tipodocumento:
            return None
        db.session.delete(tipodocumento)
        db.session.commit()
        return tipodocumento
        