import os
import sys
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
from xml.etree import ElementTree as ET
from app import create_app, db
from app.models.facultad import Facultad  # Importar tu modelo real

os.environ['FLASK_CONTEXT'] = 'development'
os.environ['TEST_DATABASE_URI'] = 'postgresql+psycopg2://matuu:matu@localhost:5432/dev_sysacad'


def importar_facultades():
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

        # Abrir el archivo XML con la codificación correcta
        with open(xml_file_path, encoding="cp1252") as f:
            tree = ET.parse(f)
        root = tree.getroot()

        registros_importados = 0
        for item in root.findall('_expxml'):
            facultad_element = item.find('facultad')  # Fijate que el tag XML coincida con lo que usás
            nombre_element = item.find('nombre')

            if facultad_element is not None and nombre_element is not None:
                try:
                    facultad_valor = int(facultad_element.text)
                    nombre_valor = nombre_element.text

                    # Creás el objeto Facultad con los datos mínimos que usás (id es autoincrement)
                    new_entry = Facultad(
                        nombre=nombre_valor,
                        abreviatura=item.find('abreviatura').text if item.find('abreviatura') is not None else None,   
                        directorio=item.find('directorio').text if item.find('directorio') is not None else None,
                        sigla=item.find('sigla').text if item.find('sigla') is not None else None,
                        codigo_postal=item.find('codigo_postal').text if item.find('codigo_postal') is not None else None,
                        ciudad=item.find('ciudad').text if item.find('ciudad') is not None else None,
                        domicilio=item.find('domicilio').text if item.find('domicilio') is not None else None,
                        telefono=item.find('telefono').text if item.find('telefono') is not None else None,
                        contacto=item.find('contacto').text if item.find('contacto') is not None else None,
                        email=item.find('email').text if item.find('email') is not None else None,
                        codigo=item.find('codigo').text if item.find('codigo') is not None else None
                    )

                    db.session.add(new_entry)
                    registros_importados += 1
                except Exception as e:
                    print(f"Error al procesar item: {ET.tostring(item, encoding='unicode')}\n{e}")
            else:
                print(f"Skipping item por falta de 'facultad' o 'nombre': {ET.tostring(item, encoding='unicode')}")

        db.session.commit()
        print(f"Importación finalizada. Registros insertados: {registros_importados}")

if __name__ == '__main__':
    importar_facultades()
