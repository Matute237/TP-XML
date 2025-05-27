import sys
import xml.etree.ElementTree as ET
from app import create_app, db
from app.models.facultad import Facultad

def importar_facultades(xml_path: str):
    """
    Importa facultades desde un archivo XML al modelo Facultad.
    """
    app = create_app()  # Crear instancia de la app
    with app.app_context():
        tree = ET.parse(xml_path)
        root = tree.getroot()

        for facultad_elem in root.findall("facultad"):
            nombre = facultad_elem.find("nombre").text
            codigo = facultad_elem.find("codigo").text

            nueva_facultad = Facultad(nombre=nombre, codigo=codigo)
            db.session.add(nueva_facultad)

        db.session.commit()
        print(f"Facultades importadas desde {xml_path} correctamente.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python scrips/import_facultades.py archivo.xml")
        sys.exit(1)

    ruta_xml = sys.argv[1]
    importar_facultades(ruta_xml)
