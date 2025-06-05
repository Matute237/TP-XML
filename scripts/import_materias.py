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
from app.models.materia import Materia
import funcion_decode

def importar_materias():
    # Configuraciones de entorno
    os.environ['FLASK_CONTEXT'] = 'development'
    os.environ['TEST_DATABASE_URI'] = 'postgresql+psycopg2://matuu:matu@localhost:5432/dev_sysacad?client_encoding=UTF8&options=-csearch_path%3Dpublic'

    app = create_app()
    with app.app_context():
        db.create_all()

        # Ruta del XML
        xml_file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'archivados_xml', 'materias.xml')
        )

        if not os.path.exists(xml_file_path):
            print(f"ERROR: No se encontró el archivo XML: {xml_file_path}")
            return

        print(f"Importando desde: {xml_file_path}")
        
        try:
            # Crear un parser más permisivo
            parser = ET.XMLParser(encoding='cp1252')
            
            # Leer y limpiar el contenido del archivo
            with open(xml_file_path, 'r', encoding='cp1252', errors='replace') as file:
                content = file.read()
                # Reemplazar caracteres problemáticos
                content = content.replace('�', '')
                
            # Parsear el contenido limpio
            root = ET.fromstring(content, parser=parser)
        except ET.ParseError as e:
            print(f"Error al parsear el archivo XML: {e}")
            print(f"Posición del error: línea {e.position[0]}, columna {e.position[1]}")
            return
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
            return

        registros_importados = 0
        registros_duplicados = 0
        registros_error = 0

        for item in root.findall('_expxml'):
            materia_element = item.find('materia')
            nombre_element = item.find('nombre')

            if materia_element is not None and nombre_element is not None:
                try:
                    materia_id = int(materia_element.text)
                    nombre = funcion_decode.decode_win1252(nombre_element.text)
                    
                    # Obtener los campos adicionales del XML
                    especialidad = int(item.find('especialidad').text) if item.find('especialidad') is not None and item.find('especialidad').text else None
                    plan = int(item.find('plan').text) if item.find('plan') is not None and item.find('plan').text else None
                    materia_code = funcion_decode.decode_win1252(item.find('materia').text) if item.find('materia') is not None and item.find('materia').text else None
                    ano = int(item.find('ano').text) if item.find('ano') is not None and item.find('ano').text else None

                    # Verificar si ya existe
                    existing = Materia.query.get(materia_id)
                    if existing:
                        print(f"Registro duplicado ID {materia_id}: {nombre}")
                        registros_duplicados += 1
                        continue

                    # Crear nueva materia
                    new_entry = Materia(
                        id=materia_id,
                        especialidad=especialidad,
                        plan=plan,
                        materia=materia_code,
                        nombre=nombre,
                        ano=ano
                    )

                    # Mostrar los datos antes de guardar
                    print("\n=== Datos a guardar ===")
                    print(f"ID: {new_entry.id}")
                    print(f"Especialidad: {new_entry.especialidad}")
                    print(f"Plan: {new_entry.plan}")
                    print(f"Materia: {new_entry.materia}")
                    print(f"Nombre: {new_entry.nombre}")
                    print(f"Año: {new_entry.ano}")
                    print("=" * 50)

                    db.session.add(new_entry)
                    db.session.commit()
                    registros_importados += 1

                except ValueError:
                    db.session.rollback()
                    print(f"Error: El valor de materia no es un número válido: {materia_element.text}")
                    registros_error += 1
                except IntegrityError:
                    db.session.rollback()
                    print(f"Error de integridad al insertar materia {materia_id}")
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
    importar_materias()