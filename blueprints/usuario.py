from flask import Blueprint, jsonify, request
from model.usuario import Usuario
from db import db
import bcrypt

usuario = Blueprint('usuario', __name__)

@usuario.route('/api/usuarios')
def obtener_usuarios():
    usuarios = Usuario.query.filter().all()
    usuarios = list(map(lambda u: u.to_dict(), usuarios))
    return jsonify(
        {
            'status': 'Ok',
            'message': 'Usuarios obtenidos correctamente',
            'data': usuarios
        }
    ), 200

@usuario.route('/api/usuarios/', methods=['POST'])
def crear_usuarios():
    res = request.get_json()
    # Todo: validad schema del json
    old_user = Usuario.query.get(res['rut'])
    if(old_user is None and res):
        hashed_pw = bcrypt.hashpw(res['passwrd'].encode('utf-8'), bcrypt.gensalt())
        new_user = Usuario(rut=res['rut'], nombre=res['nombre'],apellidos=res['apellidos'],direccion=res['direccion'], telefono=res['telefono'], correo=res['correo'],passwrd=hashed_pw,genero=res['genero'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify(
            {
                'status': 'OK',
                'message': 'Usuario registrado correctamente'
            }
        )
    return jsonify(
        {
            'status': 'Error',
            'message': 'Usuario ya registrado'
        }
    )