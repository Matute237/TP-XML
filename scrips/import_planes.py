import sys
import os
import locale

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import create_app, db
from xml.etree import ElementTree as ET
from sqlalchemy.exc import IntegrityError
from app.models.especialidad import EspecialidadModel
import funcion_decode
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Definir modelo PlanModel dentro de este archivo
class PlanModel(db.Model):
    __tablename__ = 'planes'
    id = Column(Integer, primary_key=True)
    especialidad_id = Column(Integer, ForeignKey('especialidades.id'), nullable=False)
    plan = Column(Integer, nullable=False)
    nombre = Column(String(100))

    especialidad_obj = relationship('EspecialidadModel', back_populates='planes')

# Agregar relación en EspecialidadModel si quieres (opcional)
if not hasattr(EspecialidadModel, 'planes'):
    EspecialidadModel.planes = relationship('PlanModel', back_populates='especialidad_obj', cascade="all, delete-orphan")

def importar_planes():
    os.environ['FLASK_CONTEXT'] = 'testing'
    locale.setlocale(locale.LC_ALL, 'Spanish_Spain.1252')
    sys.stdout.reconfigure(encoding='utf-8')

    app = create_app()
    with app.app_context():
        db.create_all()

        xml_file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'archivados_xml', 'planes.xml')
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
            plan_element = item.find('plan')
            nombre_element = item.find('nombre')

            if especialidad_element is not None and plan_element is not None:
                try:
                    especialidad_id = int(especialidad_element.text)
                    plan_num = int(plan_element.text)
                    nombre = funcion_decode.decode_win1252(nombre_element.text) if nombre_element is not None else None

                    # Verificar que especialidad existe
                    especialidad = EspecialidadModel.query.get(especialidad_id)
                    if not especialidad:
                        print(f"Error: especialidad ID {especialidad_id} no existe. Saltando plan.")
                        registros_error += 1
                        continue

                    # Verificar si plan ya existe para esa especialidad
                    existing = PlanModel.query.filter_by(especialidad_id=especialidad_id, plan=plan_num).first()
                    if existing:
                        print(f"Registro duplicado Plan {plan_num} para Especialidad {especialidad_id}: {nombre}")
                        registros_duplicados += 1
                        continue

                    new_plan = PlanModel(
                        especialidad_id=especialidad_id,
                        plan=plan_num,
                        nombre=nombre
                    )

                    db.session.add(new_plan)
                    db.session.commit()
                    registros_importados += 1

                    # Mostrar registro guardado
                    print(f"Guardado Plan ID {new_plan.id}: Especialidad {new_plan.especialidad_id}, Plan {new_plan.plan}, Nombre: {new_plan.nombre}")


                except ValueError:
                    db.session.rollback()
                    print(f"Error: valores inválidos especialidad {especialidad_element.text} o plan {plan_element.text}")
                    registros_error += 1
                except IntegrityError:
                    db.session.rollback()
                    print(f"Error de integridad al insertar plan {plan_num} para especialidad {especialidad_id}")
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
    importar_planes()
