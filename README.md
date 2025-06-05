# 🧾 Proyecto de Importación XML con Flask

Este proyecto es una aplicación construida con Flask que permite importar datos desde archivos XML y cargarlos en una base de datos usando SQLAlchemy.

## 📁 Estructura del proyecto
Aqui estan las raices mas importantes que se utilizan
├── app/ # aplicación Flask
│ ├── models/ # modelos de SQLAlchemy
│ └── ...
├── archivados_xml/ # archivos XML a importar
├── scripts/ # scripts de importación y ejecución
│ ├── import_*.py
│ └── cargatodo.py
├── README.md
└── ...
---

## Instalacion

### 1. Clonar el repositorio
Si no tienes GIT
    •Descargalo https://github.com/Matute237/TP-XML 
    y lo descomprimes donde quieras guardarlo
Si tienes Git
    •```bash
    git clone https://github.com/Matute237/TP-XML 
    cd ruta_donde_guardes_el_repositorio

## Crear un entorno virtual (NO es obligatorio)
•En cmd
python -m venv venv
source venv/bin/activate    # Linux/macOS
venv\Scripts\activate.bat   # Windows

## Instala requerimientos
pip install -r requirements.txt

## Configura tu env
TEST_DATABASE_URI='postgresql+psycopg2://tu_usuario:tu_contaseña@localhost:5432/test_sysacad'
DEV_DATABASE_URI='postgresql+psycopg2://tu_usuario:tu_contraseña@localhost:5432/dev_sysacad'

## Ejecutar los Scripts
Una vez realizaste todo lo anterior, para cargar los archivos
Verifica:
    •En cmd estes en la ruta donde descomprimiste el repositorio
    •Estan todos los archivos

•Una vez este todo, ejecuta
python scripts/cargatodo.py

Si configuraste bien tu env, se cargaran TODOS los datos en sus tablas correspondientes en tu base de datos

•Si deseas hacerlo individual ejecuta, por ejemplo
python scripts/import_especialidades.py

## 👨‍💻 Autores
•Andino Nicolás Legajo N° 9935
•Assenza Ezequiel Legajo N° 9943
•Lopez Matias Legajo N° 10097
•Orellana Lucas Legajo N° 10163




