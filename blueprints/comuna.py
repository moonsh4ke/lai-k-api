from flask import Blueprint, jsonify, request
from model import Comuna, db

comuna = Blueprint('comuna', __name__)

@comuna.route('/api/comunas')
def obtener_comunas():
    comunas = Comuna.query.all()
    comunas = list(map(lambda c: c.nombre, comunas))

    return jsonify(
        {
            'status': 'Ok',
            'message': 'Comunas obtenidas correctamente',
            'data': comunas
        }
    ), 200
