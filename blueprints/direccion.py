from flask import Blueprint, jsonify, request
from model import Usuario, Profesional, Direccion, db
from app import db
import bcrypt

direccion = Blueprint('direccion', __name__)

@direccion.route('/api/direccion') # METODO GET
def obtener_direcciones():
    direccion = Direccion.query.all()
    direccion = list(map(lambda d: {"id": d.id, "calle": d.calle, "comuna": d.comuna, "numero": d.numero}, direccion))

    return jsonify(
        {
            'status': 'Ok',
            'message': 'Direcciones obtenidas correctamente',
            'data': direccion
        }
    ), 200