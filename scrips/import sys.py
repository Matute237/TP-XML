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

class PlanModel(db.Model):
    __tablename__ = 'planes'
    id = Column(Integer, primary_key=True)
    especialidad_id = Column(Integer, ForeignKey('especialidades.id'), nullable=False)
    plan = Column(Integer, nullable=False)
    nombre = Column(String(100))

    especialidad_obj = relationship('EspecialidadModel', back_populates='planes')
    
# Definición del modelo GradoModel
class GradoModel(db.Model):
    _tablename_ = 'grados'
    id = Column(Integer, primary_key=True)
    especialidad_id = Column(Integer, ForeignKey('especialidades.id'), nullable=False)
    plan_id = Column(Integer, ForeignKey('planes.id'), nullable=False)
    materia = Column(Integer, nullable=True)
    grado = Column(Integer, nullable=False)
    nombre = Column(String(100))

    especialidad = relationship('EspecialidadModel', back_populates='grados')
    plan = relationship('PlanModel', back_populates='grados')

# Agregar relaciones inversas si no existen
if not hasattr(EspecialidadModel, 'grados'):
    EspecialidadModel.grados = relationship('GradoModel', back_populates='especialidad', cascade="all, delete-orphan")

if not hasattr(PlanModel, 'grados'):
    PlanModel.grados = relationship('GradoModel', back_populates='plan', cascade="all, delete-orphan")

def importar_grados():
    os.environ['FLASK_CONTEXT'] = 'development'
    os.environ['TEST_DATABASE_URI'] = 'postgresql+psycopg2://matuu:matu@localhost:5432/dev_sysacad?client_encoding=UTF8&options=-csearch_path%3Dpublic'
    locale.setlocale(locale.LC_ALL, 'Spanish_Spain.1252')
    sys.stdout.reconfigure(encoding='utf-8')

    app = create_app()
    with app.app_context():
        db.create_all()

        xml_file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'archivados_xml', 'grados.xml')
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
            materia_element = item.find('materia')
            grado_element = item.find('ano')
            nombre_element = item.find('nombre')

            if especialidad_element is not None and plan_element is not None and grado_element is not None:
                try:
                    especialidad_id = int(especialidad_element.text)
                    plan_num = int(plan_element.text)
                    materia_num = int(materia_element.text) if materia_element is not None else None
                    grado_num = int(grado_element.text)
                    nombre = funcion_decode.decode_win1252(nombre_element.text) if nombre_element is not None else None

                    especialidad = EspecialidadModel.query.get(especialidad_id)
                    if not especialidad:
                        print(f"Error: especialidad ID {especialidad_id} no existe. Saltando grado.")
                        registros_error += 1
                        continue

                    plan = PlanModel.query.filter_by(especialidad_id=especialidad_id, plan=plan_num).first()
                    if not plan:
                        print(f"Error: plan {plan_num} para especialidad {especialidad_id} no existe. Saltando grado.")
                        registros_error += 1
                        continue

                    existing = GradoModel.query.filter_by(
                        especialidad_id=especialidad_id,
                        plan_id=plan.id,
                        materia=materia_num,
                        grado=grado_num
                    ).first()
                    if existing:
                        print(f"Registro duplicado Grado (Especialidad {especialidad_id}, Plan {plan_num}, Materia {materia_num}, Grado {grado_num}): {nombre}")
                        registros_duplicados += 1
                        continue

                    new_grado = GradoModel(
                        especialidad_id=especialidad_id,
                        plan_id=plan.id,
                        materia=materia_num,
                        grado=grado_num,
                        nombre=nombre
                    )
                    db.session.add(new_grado)
                    db.session.commit()
                    registros_importados += 1
                    print(f"Guardado Grado ID {new_grado.id}: Especialidad {especialidad_id}, Plan {plan_num}, Materia {materia_num}, Grado {grado_num}, Nombre: {nombre}")

                except ValueError:
                    db.session.rollback()
                    print(f"Error: valores inválidos en especialidad, plan, materia o grado")
                    registros_error += 1
                except IntegrityError:
                    db.session.rollback()
                    print(f"Error de integridad al insertar grado")
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

if __name__ == '_main_':
    importar_grados()