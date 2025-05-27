import unittest
import tempfile
import os
from app import create_app, db
from app.models.facultad import Facultad
from scrips.import_facultades import importar_facultades

class TestImportFacultades(unittest.TestCase):
    def setUp(self):
        """
        Crear una app de test y base de datos en memoria
        """
        self.app = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['TESTING'] = True

        with self.app.app_context():
            db.create_all()

        self.client = self.app.test_client()

        # Crear XML temporal con una facultad
        self.test_xml = tempfile.NamedTemporaryFile(delete=False, suffix=".xml", mode='w', encoding='windows-1252')
        self.test_xml.write('''<?xml version="1.0" encoding="windows-1252"?>
<facultades>
    <facultad>
        <nombre>Facultad de Ingeniería</nombre>
        <codigo>FI001</codigo>
    </facultad>
</facultades>
''')
        self.test_xml.close()

    def tearDown(self):
        """
        Eliminar archivo temporal y limpiar la DB
        """
        with self.app.app_context():
            db.drop_all()

        os.unlink(self.test_xml.name)

    def test_importar_facultades(self):
        """
        Testea que se importe correctamente una facultad desde XML
        """
        with self.app.app_context():
            importar_facultades(self.test_xml.name)

            facultades = Facultad.query.all()
            self.assertEqual(len(facultades), 1)
            self.assertEqual(facultades[0].nombre, "Facultad de Ingeniería")
            self.assertEqual(facultades[0].codigo, "FI001")

if __name__ == "__main__":
    unittest.main()
