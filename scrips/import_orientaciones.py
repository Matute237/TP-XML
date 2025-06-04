import sys
import os
import locale

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# configurar codificación y entorno
locale.setlocale(locale.LC_ALL, 'Spanish_Spain.1252')
sys.stdout.reconfigure(encoding='utf-8')

from app import create_app, db
from xml.etree import ElementTree as ET
from sqlalchemy.exc import IntegrityError
import funcion_decode
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models.especialidad import EspecialidadModel

# modelo orientacion
class OrientacionModel(db.Model):
    __tablename__ = ''
    id = Column(Integer, primary_key=True)
    especialidad_id = Column(Integer, ForeignKey('especialidades.id'), nullable=False)
    plan = Column(Integer, nullable=False)
    nombre = Column(String(150), nullable=True)

    especialidad_obj = relationship('EspecialidadModel', back_populates='orientaciones')

if not hasattr(EspecialidadModel, 'orientaciones'):
    EspecialidadModel.orientaciones = relationship('OrientacionModel', back_populates='especialidad_obj', cascade="all, delete-orphan")

def importar_orientaciones():
    os.environ['FLASK_CONTEXT'] = 'development'

    app = create_app()
    with app.app_context():
        db.create_all()

        xml_file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'archivados_xml', 'orientaciones.xml')
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
            esp_el = item.find('especialidad')
            plan_el = item.find('plan')
            nombre_el = item.find('nombre')

            if esp_el is not None and plan_el is not None:
                try:
                    especialidad_id = int(esp_el.text)
                    plan_num = int(plan_el.text)
                    nombre = funcion_decode.decode_win1252(nombre_el.text) if nombre_el is not None else None

                    especialidad = EspecialidadModel.query.get(especialidad_id)
                    if not especialidad:
                        print(f"Error: especialidad ID {especialidad_id} no existe. Saltando registro.")
                        registros_error += 1
                        continue

                    existing = OrientacionModel.query.filter_by(
                        especialidad_id=especialidad_id,
                        plan=plan_num,
                    ).first()

                    if existing:
                        print(f"Registro duplicado para Plan {plan_num} y Especialidad {especialidad_id}: {nombre}")
                        registros_duplicados += 1
                        continue

                    nueva_orientacion = OrientacionModel(
                        especialidad_id=especialidad_id,
                        plan=plan_num,
                        nombre=nombre
                    )

                    db.session.add(nueva_orientacion)
                    db.session.commit()
                    registros_importados += 1
                    print(f"Guardado Orientación ID {nueva_orientacion.id}: Esp {especialidad_id}, Plan {plan_num}, Nombre: {nombre}")

                except ValueError:
                    db.session.rollback()
                    print(f"Error: valores inválidos en especialidad o plan: {esp_el.text}, {plan_el.text}")
                    registros_error += 1
                except IntegrityError:
                    db.session.rollback()
                    print(f"Error de integridad al insertar para plan {plan_num} y especialidad {especialidad_id}")
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
    importar_orientaciones()
