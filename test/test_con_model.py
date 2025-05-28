import os
import sys
import unittest
from xml.etree import ElementTree as ET

# Agregar el path del proyecto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Variables de entorno necesarias para Flask
os.environ['FLASK_CONTEXT'] = 'testing'
os.environ['TEST_DATABASE_URI'] = 'postgresql+psycopg2://nico:nicoS@localhost:5432/test_sysacad'

from app import create_app, db
from app.models.facultad import Facultad

class TestImportFacultades(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Se ejecuta una vez antes de todos los tests"""
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        with cls.app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Se ejecuta una vez después de todos los tests"""
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_importar_facultades(self):
        """Testea que se puedan importar facultades desde el XML"""
        xml_file_path = os.path.join(BASE_DIR, 'archivados_xml', 'facultades.xml')
        self.assertTrue(os.path.exists(xml_file_path), f"XML no encontrado: {xml_file_path}")

        with open(xml_file_path, 'r', encoding='windows-1252') as f:
            tree = ET.parse(f)
        root = tree.getroot()

        registros_importados = 0
        with self.app.app_context():
            for item in root.findall('_expxml'):
                nombre_valor = item.findtext('nombre')
                if not nombre_valor:
                    continue

                nueva_facultad = Facultad(
                    nombre=nombre_valor,
                    abreviatura=item.findtext('abreviatura'),
                    directorio=item.findtext('directorio'),
                    sigla=item.findtext('sigla'),
                    codigo_postal=item.findtext('codigo_postal'),
                    ciudad=item.findtext('ciudad'),
                    domicilio=item.findtext('domicilio'),
                    telefono=item.findtext('telefono'),
                    contacto=item.findtext('contacto'),
                    email=item.findtext('email'),
                    codigo=item.findtext('codigo')
                )

                db.session.add(nueva_facultad)
                registros_importados += 1

            db.session.commit()


            total = db.session.query(Facultad).count()
            self.assertGreaterEqual(total, registros_importados, "No se insertaron registros correctamente")

if __name__ == '__main__':
    unittest.main()
