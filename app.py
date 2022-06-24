from flask import Flask
from config import config
from extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(config['development'])

    register_extensions(app)
    register_blueprint(app)
    return app

def register_extensions(app):
    db.init_app(app)

def register_blueprint(app):
    #Importa las blueprints
    from src.blueprints.auth import auth
    from src.blueprints.usuario import usuario

    # Registra las rutas en la app
    app.register_blueprint(auth)
    app.register_blueprint(usuario)

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
    