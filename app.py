import bcrypt
from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy

def create_app():
    app = Flask(__name__)
    app.config.from_object(config['development'])
    SQLAlchemy(app)

    register_blueprints(app)
    return app

def register_blueprints(app):
    register_blueprint(app)
    return app

def register_blueprint(app):
    #Importa las blueprints
    from blueprints.auth import auth
    from blueprints.usuario import usuario

    # Registra las rutas en la app
    app.register_blueprint(auth)
    app.register_blueprint(usuario)

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
