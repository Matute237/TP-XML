import os
import unittest
from sqlalchemy import text
from app import create_app, db

print("FLASK_CONTEXT en test:", os.getenv("FLASK_CONTEXT"))
print("TEST_DATABASE_URI en test:", os.getenv("TEST_DATABASE_URI"))

class ConnectionTestCase(unittest.TestCase):

    def setUp(self):
        # Configuramos el entorno de testing
        os.environ['FLASK_CONTEXT'] = 'testing'
        os.environ['TEST_DATABASE_URI'] = 'sqlite:///:memory:'  # Base de datos en memoria

        # Creamos la app y el contexto
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Inicializamos las tablas (aunque no haya modelos, esto es estándar)
        db.create_all()

    def tearDown(self):
        # Limpiamos todo después del test
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_db_connection(self):
        # Ejecutamos una consulta básica para probar conexión a la base de datos
        result = db.session.execute(text("SELECT 'Hello world'")).scalar()
        self.assertEqual(result, 'Hello world')

if __name__ == '__main__':
    unittest.main()
