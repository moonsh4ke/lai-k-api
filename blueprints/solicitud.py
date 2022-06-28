from flask import Blueprint, jsonify, request
from model import Solicitud, Notificacion, db
import datetime

solicitud = Blueprint('solicitud', __name__)

@solicitud.route('/api/solicitudes') #METODO GET
def obtener_solicitud():
    pass

@solicitud.route('/api/solicitudes', methods=['POST'])
def crear_solicitud():
    res = request.get_json()
    fecha = datetime.datetime.strptime(res['fecha_hora'], "%a, %d %b %Y %H:%M:%S %Z")
    solicitud = Solicitud(profesional_rut=res['profesional_rut'], duenio_rut=res['duenio_rut'], direccion_id=res['direccion_id'], estado_nombre="Esperando confirmacion de profesional", fecha_hora=fecha, servicio=res['servicio'])

    if 'comentario' in res:
        solicitud.comentario = res['comentario']

    notificacion = Notificacion(receptor_rut=res['profesional_rut'], emisor_rut=res['duenio_rut'], tipo_nombre="Nueva solicitud de visita", estado=True)
    notificacion.solicitud = solicitud

    db.session.add(notificacion)
    db.session.commit()

    return jsonify (
            {
                "status": "Ok",
                "message": "Solicitud registrada correctamente y notificacion generada"
            }
        ), 200
