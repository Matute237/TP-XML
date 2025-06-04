import sys
import os
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


from app import create_app, db
from xml.etree import ElementTree as ET
from sqlalchemy.exc import IntegrityError
from app.models.grado import Grado
import funcion_decode

def importar_grados():
    # Configuraciones de entorno
    os.environ['FLASK_CONTEXT'] = 'development'
    os.environ['TEST_DATABASE_URI'] = 'postgresql+psycopg2://matuu:matu@localhost:5432/dev_sysacad?client_encoding=UTF8&options=-csearch_path%3Dpublic'

    app = create_app()
    with app.app_context():
        db.create_all()

        # Ruta del XML
        xml_file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'archivados_xml', 'grados.xml')
        )

        if not os.path.exists(xml_file_path):
            print(f"ERROR: No se encontró el archivo XML: {xml_file_path}")
            return

        print(f"Importando desde: {xml_file_path}")
        
        try:
            tree = ET.parse(xml_file_path)
            root = tree.getroot()
        except ET.ParseError as e:
            print(f"Error al parsear el archivo XML: {e}")
            return

        registros_importados = 0
        registros_duplicados = 0
        registros_error = 0

        for item in root.findall('_expxml'):
            grado_element = item.find('grado')
            nombre_element = item.find('nombre')

            if grado_element is not None and nombre_element is not None:
                try:
                    grado_id = int(grado_element.text)
                    nombre = funcion_decode.decode_win1252(nombre_element.text)

                    # Verificar si ya existe
                    existing = Grado.query.get(grado_id)
                    if existing:
                        print(f"Registro duplicado ID {grado_id}: {nombre}")
                        registros_duplicados += 1
                        continue

                    # Crear nuevo grado
                    new_entry = Grado(
                        id=grado_id,
                        nombre=nombre,
                    )

                    db.session.add(new_entry)
                    db.session.commit()
                    registros_importados += 1

                except ValueError:
                    db.session.rollback()
                    print(f"Error: El valor de grado no es un número válido: {grado_element.text}")
                    registros_error += 1
                except IntegrityError:
                    db.session.rollback()
                    print(f"Error de integridad al insertar grado {grado_id}")
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
    importar_grados()