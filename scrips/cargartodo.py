# scripts/ejecutar_importaciones.py

# opcional: configuración del path base si es necesario
import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from import_especialidades import importar_especialidades
from import_facultades import importar_facultades
from import_grados import importar_grados
from import_localidades import importar_localidades
from import_materias import importar_materias
from import_orientaciones import importar_orientaciones
from import_paises import importar_paises
from import_planes import importar_planes
from import_universidad import importar_universidades

def ejecutar_todo():
    print(">>> Iniciando proceso de importación de datos XML...\n")

    importar_especialidades()
    importar_facultades()
    importar_grados()
    importar_localidades()
    importar_materias()
    importar_orientaciones()
    importar_paises()
    importar_planes()
    importar_universidades()

    print("\n>>> Proceso de importación finalizado con exito.")

if __name__ == "__main__":
    ejecutar_todo()
