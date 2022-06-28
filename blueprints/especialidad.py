from flask import Blueprint, jsonify, request
from model import Especialidad, db
import datetime

especialidad = Blueprint('especialidad', __name__)

@especialidad.route('/api/especialidades')
def obtener_especialidades():
    especialidades = Especialidad.query.all()
    especialidades = list(map(lambda e: {"nombre": e.nombre, "descripcion": e.descripcion}, especialidades))

    return jsonify(
        {
            'status': 'Ok',
            'message': 'Especialidades obtenidas correctamente',
            'data': especialidades
        }
    ), 200
