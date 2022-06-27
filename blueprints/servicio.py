from flask import Blueprint, jsonify, request
from model import Servicio, db

servicio = Blueprint('servicio', __name__)

@servicio.route('/api/servicios')
def obtener_servicios():
    servicio = Servicio.query.all()
    servicio = list(map(lambda s: s.nombre, servicio))

    return jsonify(
        {
            'status': 'Ok',
            'message': 'Servicios obtenidos correctamente',
            'data': servicio
        }
    ), 200
