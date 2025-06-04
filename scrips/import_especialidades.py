import sys
import os
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
from app import create_app, db
from xml.etree import ElementTree as ET
from sqlalchemy.exc import IntegrityError
from app.models.especialidad import EspecialidadModel
from sqlalchemy import text  # Agregar esta importación al inicio del archivo

def importar_especialidades():
    # Configuraciones de entorno
    os.environ['FLASK_CONTEXT'] = 'development'
    os.environ['TEST_DATABASE_URI'] = 'postgresql+psycopg2://matuu:matu@localhost:5432/dev_sysacad'

    app = create_app()
    with app.app_context():
        db.create_all()

        # Resetear la secuencia al máximo ID actual + 1
        try:
            result = db.session.execute(text("""
                SELECT setval('especialidades_id_seq', 
                    COALESCE((SELECT MAX(id) FROM especialidades), 0) + 1, false)
            """))
        except Exception as e:
            print(f"Error al resetear secuencia: {e}")
            return

        # Ruta del XML
        xml_file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'archivados_xml', 'especialidades.xml')
        )

        if not os.path.exists(xml_file_path):
            print(f"ERROR: No se encontró el archivo XML: {xml_file_path}")
            return

        print(f"Importando desde: {xml_file_path}")
        
        # Intentar parsear el XML
        try:
            tree = ET.parse(xml_file_path)
            root = tree.getroot()
        except ET.ParseError as e:
            print(f"Error al parsear el archivo XML: {e}")
            return

        registros_importados = 0
        registros_duplicados = 0
        registros_error = 0
        
        # Iterar sobre los elementos del XML
        for item in root.findall('_expxml'):
            especialidad_element = item.find('especialidad')
            nombre_element = item.find('nombre')
            
            # Verificar que los elementos existan
            if (especialidad_element is not None and nombre_element is not None):
                try:
                    especialidad = especialidad_element.text
                    nombre = nombre_element.text

                    # Verificar si ya existe
                    existing = EspecialidadModel.query.filter_by(
                        especialidad=especialidad,
                        nombre=nombre
                    ).first()

                    if existing:
                        print(f"Registro duplicado: {especialidad} - {nombre}")
                        registros_duplicados += 1
                        continue

                    # No necesitas especificar el id, se generará automáticamente
                    new_entry = EspecialidadModel(
                        especialidad=especialidad,
                        nombre=nombre
                    )
                    db.session.add(new_entry)
                    db.session.commit()
                    registros_importados += 1

                except IntegrityError:
                    db.session.rollback()
                    print(f"Error de integridad al insertar: {especialidad} - {nombre}")
                    registros_error += 1
                except Exception as e:
                    db.session.rollback()
                    print(f"Error al procesar item: {ET.tostring(item, encoding='unicode')}\n{e}")
                    registros_error += 1
            else:
                print(f"Skipeado por datos faltantes: {ET.tostring(item, encoding='unicode')}")
                registros_error += 1

        print(f"""
Importación finalizada:
- Registros insertados: {registros_importados}
- Registros duplicados: {registros_duplicados}
- Registros con error: {registros_error}
""")

if __name__ == '__main__':
    importar_especialidades()
