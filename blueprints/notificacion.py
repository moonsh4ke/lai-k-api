from flask import Blueprint, jsonify, request
from model import Usuario, Profesional, Servicio, PlanificacionDia, Dia, Notificacion, db
from app import db
import bcrypt

notificacion = Blueprint('notificacion', __name__)

@notificacion.route('/api/notificacion') # METODO GET
def obtener_notificaciones():
    notificacion = Notificacion.query.all()
    notificacion = list(map(lambda n: {"id": n.id,"estado": n.estado,"receptor rut": n.receptor_rut, "emisor rut": n.emisor_rut, "tipo nombre": n.tipo_nombre, "id solicitud": n.solicitud_id}, notificacion))

    return jsonify(
        {
            'status': 'Ok',
            'message': 'Notificaciones obtenidas correctamente',
            'data': notificacion
        }
    ), 200

@notificacion.route('/api/notificacion', methods=['POST'])
def crear_notificacion():
    return "CREANDO NOTIFICACION"
