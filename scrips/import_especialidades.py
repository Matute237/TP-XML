import sys
import os
import locale
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Configurar codificación
locale.setlocale(locale.LC_ALL, 'Spanish_Spain.1252')
sys.stdout.reconfigure(encoding='utf-8')

from app import create_app, db
from xml.etree import ElementTree as ET
from sqlalchemy.exc import IntegrityError
from app.models.especialidad import EspecialidadModel
import funcion_decode

def importar_especialidades():
    # Configuraciones de entorno
    os.environ['FLASK_CONTEXT'] = 'development'
    #os.environ['TEST_DATABASE_URI'] = 'postgresql+psycopg2://matuu:matu@localhost:5432/dev_sysacad?client_encoding=utf8'

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
        
        try:
            with open(xml_file_path, 'r', encoding='cp1252') as file:
                tree = ET.parse(file)
                root = tree.getroot()
        except ET.ParseError as e:
            print(f"Error al parsear el archivo XML: {e}")
            return

        registros_importados = 0
        registros_duplicados = 0
        registros_error = 0

        for item in root.findall('_expxml'):
            especialidad_element = item.find('especialidad')
            nombre_element = item.find('nombre')

            if especialidad_element is not None and nombre_element is not None:
                try:
                    especialidad_id = int(especialidad_element.text)
                    nombre = funcion_decode.decode_win1252(nombre_element.text)

                    # Verificar si ya existe
                    existing = EspecialidadModel.query.get(especialidad_id)
                    if existing:
                        print(f"Registro duplicado ID {especialidad_id}: {nombre}")
                        registros_duplicados += 1
                        continue

                    # Crear nueva especialidad
                    new_entry = EspecialidadModel(
                        id=especialidad_id,
                        especialidad=especialidad_id,
                        nombre=nombre,
                        letra=funcion_decode.decode_win1252(item.find('letra').text) if item.find('letra') is not None else None,
                        observacion=funcion_decode.decode_win1252(item.find('observacion').text) if item.find('observacion') is not None else None
                    )
                    
                    db.session.add(new_entry)
                    db.session.commit()
                    registros_importados += 1

                except ValueError:
                    db.session.rollback()
                    print(f"Error: El valor de especialidad no es un número válido: {especialidad_element.text}")
                    registros_error += 1
                except IntegrityError:
                    db.session.rollback()
                    print(f"Error de integridad al insertar especialidad {especialidad_id}")
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