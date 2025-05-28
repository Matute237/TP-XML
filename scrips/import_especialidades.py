import sys
import os
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import create_app, db
from xml.etree import ElementTree as ET


# Modelo Especialidad simplificado
class EspecialidadModel(db.Model):
    __tablename__ = 'especialidades'
    id = db.Column(db.Integer, primary_key=True)
    especialidad = db.Column(db.String(255), nullable=False)
    nombre = db.Column(db.String(255), nullable=False)

def importar_especialidades():
    # Configuraciones de entorno
    os.environ['FLASK_CONTEXT'] = 'testing'
    os.environ['TEST_DATABASE_URI'] = 'postgresql+psycopg2://matuu:matu@localhost:5432/test_sysacad'

    app = create_app()
    with app.app_context():
        db.create_all()

        # Ruta del XML
        xml_file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'archivados_xml', 'especialidades.xml')
        )

        if not os.path.exists(xml_file_path):
            print(f"ERROR: No se encontró el archivo XML: {xml_file_path}")
            return

        print(f"Importando desde: {xml_file_path}")

        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        registros_importados = 0
        for item in root.findall('_expxml'):
            especialidad_element = item.find('especialidad')
            nombre_element = item.find('nombre')

            if especialidad_element is not None and nombre_element is not None:
                try:
                    especialidad = especialidad_element.text
                    nombre = nombre_element.text

                    new_entry = EspecialidadModel(especialidad=especialidad, nombre=nombre)
                    db.session.add(new_entry)
                    registros_importados += 1
                except Exception as e:
                    print(f"Error al procesar item: {ET.tostring(item, encoding='unicode')}\n{e}")
            else:
                print(f"Skipeado por datos faltantes: {ET.tostring(item, encoding='unicode')}")

        db.session.commit()

        print(f"Importación finalizada. Registros insertados: {registros_importados}")

if __name__ == '__main__':
    importar_especialidades()
