from asyncio.log import logger
from dotenv import load_dotenv
from pathlib import Path
import os

basedir = os.path.abspath(Path(__file__).parents[2])
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    
    @staticmethod
    def init_app(app):
        pass

class TestConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URI', 'sqlite:///:memory:')   

class DevelopmentConfig(Config):
    TESTING = False
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI')
        
class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_RECORD_QUERIES = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URI')
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

def factory(app: str) -> Config:
    configuration = {
        'testing': TestConfig,
        'development': DevelopmentConfig,
        'production': ProductionConfig
    }
    
    return configuration[app]


print("TEST_DATABASE_URI =", os.getenv("TEST_DATABASE_URI"))
import os
from dotenv import load_dotenv
from pathlib import Path

# Ruta a la raíz del proyecto (dos niveles arriba de config.py)
basedir = Path(__file__).resolve().parents[2]
dotenv_path = basedir / '.env'

# Cargar el archivo .env
load_dotenv(dotenv_path)

# Confirmación por consola
print(">>> Cargando config.py")
print(">>> Ruta del .env:", dotenv_path)
print(">>> TEST_DATABASE_URI cargada:", os.getenv("TEST_DATABASE_URI"))
print(">>> FLASK_CONTEXT:", os.getenv("FLASK_CONTEXT"))

class Config(object):
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    @staticmethod
    def init_app(app):
        pass

class TestConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URI', 'sqlite:///:memory:')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URI')

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_RECORD_QUERIES = False
    SQLALCHEMY_DATABASE_URI = os.getenv('PROD_DATABASE_URI')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

def factory(app_context: str) -> Config:
    configuration = {
        'testing': TestConfig,
        'development': DevelopmentConfig,
        'production': ProductionConfig
    }

    config_class = configuration.get(app_context)
    if config_class is None:
        raise ValueError(f"Contexto inválido: '{app_context}'. Debe ser 'testing', 'development' o 'production'.")

    print(f">>> Configuración cargada: {app_context} ({config_class.__name__})")
    return config_class
