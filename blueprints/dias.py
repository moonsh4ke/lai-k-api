from flask import Blueprint, jsonify, request
from model import Comuna, Dia, db
import datetime

dias = Blueprint('dias', __name__)

@dias.route('/api/dias')
def obtener_dias():
    dias = Dia.query.all()
    dias = list(map(lambda d: d.nombre, dias))
    #dia = 

    return jsonify(
        {
            'status': 'Ok',
            'message': 'Dias obtenidos correctamente',
            'data': dias
        }
    ), 200