#esto es por si sale el error
#ImportError: cannot import name 'create_app' from 'app' (C:\Users\Usuario Digital\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\site-packages\app\__init__.py)
import sys
import os
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(_file_), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
