import os
import unittest
from sqlalchemy import text
from app import create_app, db
from xml.etree import ElementTree as ET

# Modelo actualizado
class MateriaModel(db.Model):
    __tablename__ = 'materias'
    id = db.Column(db.Integer, primary_key=True)
    especialidad = db.Column(db.String(255), nullable=False)
    plan = db.Column(db.String(10), nullable=False)
    materia = db.Column(db.String(255), nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    ano = db.Column(db.Integer, nullable=True)

class XMLImportTestCase(unittest.TestCase):

    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        os.environ['TEST_DATABASE_URI'] = 'postgresql+psycopg2://matuu:matu@localhost:5432/test_sysacad'

        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.drop_all()  # Limpia la base de datos antes de crear las tablas
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_import_xml_to_db(self):
        # Ruta del archivo XML
        xml_file_path = os.path.join(
            os.path.dirname(__file__), '..', 'archivados_xml', 'materias.xml'
        )

        # Verificamos que el archivo exista
        self.assertTrue(os.path.exists(xml_file_path), f"El archivo {xml_file_path} no existe.")

        try:
            # Parseamos el archivo XML
            tree = ET.parse(xml_file_path)
            root = tree.getroot()

            for item in root.findall('_expxml'):
                especialidad_element = item.find('especialidad')
                plan_element = item.find('plan')
                materia_element = item.find('materia')
                nombre_element = item.find('nombre')
                ano_element = item.find('ano')

                # Aseguramos que los elementos requeridos no sean None
                if (especialidad_element is not None and 
                    plan_element is not None and 
                    materia_element is not None and 
                    nombre_element is not None):
                    
                    especialidad = especialidad_element.text.strip()
                    plan = plan_element.text.strip()
                    materia = materia_element.text.strip()
                    nombre = nombre_element.text.strip()
                    
                    # Convertir año a entero si existe, sino None
                    try:
                        ano = int(ano_element.text.strip()) if ano_element is not None else None
                    except (ValueError, AttributeError):
                        ano = None
                        print(f"Advertencia: Año inválido para materia {materia}, se establece como None")

                    # Insertamos en la base de datos
                    new_entry = MateriaModel(
                        especialidad=especialidad,
                        plan=plan,
                        materia=materia,
                        nombre=nombre,
                        ano=ano
                    )
                    db.session.add(new_entry)
                else:
                    print(f"skipeo el item por que falta algun dato. Especialidad: {especialidad_element}, "
                          f"Plan: {plan_element}, Materia: {materia_element}, "
                          f"Nombre: {nombre_element}, Año: {ano_element}")

            db.session.commit()

            # Verificamos que los datos se hayan insertado correctamente
            results = MateriaModel.query.all()
            self.assertGreater(len(results), 0, "No se insertaron datos en la base de datos.")
            for result in results:
                print(f"Especialidad: {result.especialidad}, Plan: {result.plan}, "
                      f"Materia: {result.materia}, Nombre: {result.nombre}, "
                      f"Año: {result.ano}")

        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al procesar el archivo XML: {str(e)}")

if __name__ == '__main__':
    unittest.main()