import sys
import os
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
from app import create_app, db
from xml.etree import ElementTree as ET
from sqlalchemy.exc import IntegrityError
from app.models.facultad import Facultad
import funcion_decode

def importar_facultades():
    # Configuraciones de entorno
    os.environ['FLASK_CONTEXT'] = 'development'
    os.environ['TEST_DATABASE_URI'] = 'postgresql+psycopg2://matuu:matu@localhost:5432/dev_sysacad?client_encoding=utf8'

    app = create_app()
    with app.app_context():
        db.create_all()

        # Ruta del XML
        xml_file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'archivados_xml', 'facultades.xml')
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
            facultad_element = item.find('facultad')
            nombre_element = item.find('nombre')

            if facultad_element is not None and nombre_element is not None:
                try:
                    facultad_id = int(facultad_element.text)
                    nombre = funcion_decode.decode_win1252(nombre_element.text)

                    # Verificar si ya existe
                    existing = Facultad.query.get(facultad_id)
                    if existing:
                        print(f"Registro duplicado ID {facultad_id}: {nombre}")
                        registros_duplicados += 1
                        continue

                    # Crear nueva facultad usando funcion_decode.decode_win1252 en cada campo de texto
                    new_entry = Facultad(
                        id=facultad_id,
                        nombre=nombre,
                        abreviatura=funcion_decode.decode_win1252(item.find('abreviatura').text) if item.find('abreviatura') is not None else None,   
                        directorio=funcion_decode.decode_win1252(item.find('directorio').text) if item.find('directorio') is not None else None,
                        sigla=funcion_decode.decode_win1252(item.find('sigla').text) if item.find('sigla') is not None else None,
                        codigo_postal=funcion_decode.decode_win1252(item.find('codigo_postal').text) if item.find('codigo_postal') is not None else None,
                        ciudad=funcion_decode.decode_win1252(item.find('ciudad').text) if item.find('ciudad') is not None else None,
                        domicilio=funcion_decode.decode_win1252(item.find('domicilio').text) if item.find('domicilio') is not None else None,
                        telefono=funcion_decode.decode_win1252(item.find('telefono').text) if item.find('telefono') is not None else None,
                        contacto=funcion_decode.decode_win1252(item.find('contacto').text) if item.find('contacto') is not None else None,
                        email=funcion_decode.decode_win1252(item.find('email').text) if item.find('email') is not None else None,
                        codigo=funcion_decode.decode_win1252(item.find('codigo').text) if item.find('codigo') is not None else None
                    )

                    # Mostrar los datos antes de guardar
                    print("\n=== Datos a guardar ===")
                    print(f"ID: {new_entry.id}")
                    print(f"Nombre: {new_entry.nombre}")
                    print(f"Abreviatura: {new_entry.abreviatura}")
                    print(f"Directorio: {new_entry.directorio}")
                    print(f"Sigla: {new_entry.sigla}")
                    print(f"Código Postal: {new_entry.codigo_postal}")
                    print(f"Ciudad: {new_entry.ciudad}")
                    print(f"Domicilio: {new_entry.domicilio}")
                    print(f"Teléfono: {new_entry.telefono}")
                    print(f"Contacto: {new_entry.contacto}")
                    print(f"Email: {new_entry.email}")
                    print(f"Código: {new_entry.codigo}")
                    print("=" * 50)

                    db.session.add(new_entry)
                    db.session.commit()
                    registros_importados += 1

                except ValueError:
                    db.session.rollback()
                    print(f"Error: El valor de facultad no es un número válido: {facultad_element.text}")
                    registros_error += 1
                except IntegrityError:
                    db.session.rollback()
                    print(f"Error de integridad al insertar facultad {facultad_id}")
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
    importar_facultades()
