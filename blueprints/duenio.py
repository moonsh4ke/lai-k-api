from flask import Blueprint, jsonify, request
from model import Usuario, Duenio, Direccion, db
import bcrypt

duenio = Blueprint('duenio', __name__)


@duenio.route('/api/duenios')
def obtener_duenios():
    duenio = Duenio.query.all()
    duenio = list(map(lambda d: d.to_dict(), duenio))
    return jsonify(
        {
            'status': 'Ok',
            'message': 'Dueños obtenidos correctamente',
            'data': duenio
        }
    ), 200


@duenio.route('/api/duenios/', methods=['POST'])
def crear_duenio():
    res = request.get_json()
    # Todo: validad schema del json
    old_user = Usuario.query.get(res['rut'])
    if(old_user is None and res):
        hashed_pw = bcrypt.hashpw(
            res['passwrd'].encode('utf-8'), bcrypt.gensalt())

        direccion = Direccion(
            calle=res['direccion']['calle'], numero=res['direccion']['numero'], comuna=res['direccion']['comuna'])

        new_user = Usuario(rut=res['rut'], nombre=res['nombre'], apellidos=res['apellidos'],
                           telefono=res['telefono'], correo=res['correo'], passwrd=hashed_pw, genero=res['genero'], direccion=direccion)

        duenio = Duenio(new_user)
        db.session.add(duenio)
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
