# Json Web Token
import jwt
# Funcion de hashing
import bcrypt
from flask import Blueprint, jsonify, request
from src.service.token_required import token_required
from config import config
from extensions import db
# Tiempo para la expiracion del token
import datetime

auth = Blueprint('auth', __name__)


@auth.route('api/login', methods=['POST'])
def login():
    res = request.get_json()
    rut = res["user"]
    password = res["password"]

    cursor = db.connection.cursor()
    query = f"SELECT * FROM usuario WHERE rut = {rut}"
    cursor.execute(query)
    usuario = cursor.fetchone()

    if res and bcrypt.checkpw(password, usuario[5].encode('utf-8')):
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow,
            'sub': rut
        }
        token = jwt.encode(payload,
                           config['development'].SECRET_KEY,
                           algorithm="HS256"
                           )
        return jsonify(
            {
                'status': 'Ok',
                'message': 'Auth exitoso',
                'token': token,
            }
        ), 200
    return jsonify(
        {
            'status': 'Error',
            'message': 'Usuario o contraseña incorrecto'
        }, 400
    )


@auth.route('/api/validateToken', methods=['GET'])
@token_required
def validateToken():
    return jsonify({
        'status': 'Ok',
        'message': 'Auth exitoso'
    }), 200
