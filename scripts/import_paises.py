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
import funcion_decode
from dataclasses import dataclass

@dataclass(init=False, repr=True, eq=True)
class Pais(db.Model):
    __tablename__ = 'paises'
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    nombre = db.Column(db.String(100), nullable=False)

def importar_paises():
    # Configuraciones de entorno
    os.environ['FLASK_CONTEXT'] = 'development'
    os.environ['TEST_DATABASE_URI'] = 'postgresql+psycopg2://matuu:matu@localhost:5432/dev_sysacad?client_encoding=UTF8&options=-csearch_path%3Dpublic'

    app = create_app()
    with app.app_context():
        db.create_all()

        # Ruta del XML
        xml_file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'archivados_xml', 'paises.xml')
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
            pais_element = item.find('pais')
            nombre_element = item.find('nombre')

            if pais_element is not None and nombre_element is not None:
                try:
                    pais_id = int(pais_element.text)
                    nombre = funcion_decode.decode_win1252(nombre_element.text)

                    # Verificar si ya existe
                    existing = Pais.query.get(pais_id)
                    if existing:
                        print(f"Registro duplicado ID {pais_id}: {nombre}")
                        registros_duplicados += 1
                        continue

                    # Crear nuevo país
                    new_entry = Pais(
                        id=pais_id,
                        nombre=nombre
                    )

                    db.session.add(new_entry)
                    db.session.commit()
                    registros_importados += 1

                except ValueError:
                    db.session.rollback()
                    print(f"Error: El valor de país no es un número válido: {pais_element.text}")
                    registros_error += 1
                except IntegrityError:
                    db.session.rollback()
                    print(f"Error de integridad al insertar país {pais_id}")
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
    importar_paises()