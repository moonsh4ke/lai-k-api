from flask import Flask
from config import config
from extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(config['development'])

    register_extensions(app)
    register_blueprints(app)
    return app

def register_extensions(app):
    db.init_app(app)

def register_blueprints(app):
    #Importa las blueprints
    from src.blueprints.auth import auth
    from src.blueprints.usuario import usuario

    # Registra las rutas en la app
    app.register_blueprints(auth)
    app.register_blueprints(usuario)

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
