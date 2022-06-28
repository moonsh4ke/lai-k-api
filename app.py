from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(config['development'])
db = SQLAlchemy(app)

def register_blueprint(app):
    # Importa las blueprints
    from blueprints.auth import auth
    # from blueprints.usuario import usuario
    # from blueprints.notificacion import notificacion
    from blueprints.solicitud import solicitud
    from blueprints.profesional import profesional
    from blueprints.comuna import comuna
    from blueprints.servicio import servicio
    from blueprints.duenio import duenio
    from blueprints.dias import dias
    from blueprints.especialidad import especialidad

    # Registra las rutas en la app
    app.register_blueprint(auth)
    # app.register_blueprint(usuario)
    # app.register_blueprint(notificacion)
    app.register_blueprint(solicitud)
    app.register_blueprint(profesional)
    app.register_blueprint(duenio)
    app.register_blueprint(comuna)
    app.register_blueprint(servicio)
    app.register_blueprint(dias)
    app.register_blueprint(especialidad)
    
register_blueprint(app)
