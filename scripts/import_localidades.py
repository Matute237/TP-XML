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
class Localidad(db.Model):
    __tablename__ = 'localidades'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo = db.Column(db.Integer, nullable=False)
    ciudad = db.Column(db.String(100), nullable=False)
    provincia = db.Column(db.String(50), nullable=True)
    pais = db.Column(db.String(50), nullable=True)

def importar_localidades():
    # Configuraciones de entorno
    os.environ['FLASK_CONTEXT'] = 'development'
    os.environ['TEST_DATABASE_URI'] = 'postgresql+psycopg2://matuu:matu@localhost:5432/dev_sysacad?client_encoding=UTF8&options=-csearch_path%3Dpublic'

    app = create_app()
    with app.app_context():
        db.create_all()

        # Ruta del XML
        xml_file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'archivados_xml', 'localidades.xml')
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

        for item in root.findall('_exportar'):
            codigo_element = item.find('codigo')
            ciudad_element = item.find('ciudad')

            if codigo_element is not None and ciudad_element is not None:
                try:
                    codigo = int(codigo_element.text)
                    ciudad = funcion_decode.decode_win1252(ciudad_element.text)

                    # Verificar si ya existe
                    existing = Localidad.query.get(codigo)
                    if existing:
                        print(f"Registro duplicado ID {codigo}: {ciudad}")
                        registros_duplicados += 1
                        continue

                    # Crear nueva localidad
                    new_entry = Localidad(
                        id=codigo,
                        codigo=codigo,
                        ciudad=ciudad,
                        provincia=funcion_decode.decode_win1252(item.find('provincia').text) if item.find('provincia') is not None else None,
                        pais=funcion_decode.decode_win1252(item.find('pais_del_c').text) if item.find('pais_del_c') is not None else None
                    )

                    db.session.add(new_entry)
                    db.session.commit()
                    registros_importados += 1

                except ValueError:
                    db.session.rollback()
                    print(f"Error: El valor de código no es un número válido: {codigo_element.text}")
                    registros_error += 1
                except IntegrityError:
                    db.session.rollback()
                    print(f"Error de integridad al insertar localidad {codigo}")
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
    importar_localidades()