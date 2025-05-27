import logging
from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from app.config import config
from dotenv import load_dotenv

# Cargar variables del .env para que os.getenv funcione
load_dotenv()

db = SQLAlchemy()

def create_app() -> Flask:
    """
    Factory para crear la app Flask con configuración según FLASK_CONTEXT
    """

    # Leer variable de entorno que indica el contexto
    app_context = os.getenv('FLASK_CONTEXT', 'development').lower()
    print(f"[DEBUG] FLASK_CONTEXT: {app_context}")

    # Mostrar la URI de la base de datos de test (por ejemplo)
    print(f"[DEBUG] TEST_DATABASE_URI: {os.getenv('TEST_DATABASE_URI')}")

    # Crear la app
    app = Flask(__name__)

    # Obtener la configuración según el contexto
    f = config.factory(app_context)
    print(f"[DEBUG] Config cargada: {f}")

    # Cargar la configuración en Flask
    app.config.from_object(f)

    # Inicializar la base de datos con la app
    db.init_app(app)

    @app.shell_context_processor
    def ctx():
        # Variables disponibles en el shell de Flask
        return {"app": app, "db": db}

    return app
