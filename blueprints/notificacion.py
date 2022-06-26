from flask import Blueprint, jsonify, request
from model.notificacion import Notificacion
from db import db
import bcrypt

notificacion = Blueprint('notificacion', __name__)

@notificacion.route('/api/notificacion') # METODO GET
def obtener_notificaciones():
    return "OBTENIENDO NOTIFICACIONES!"

@notificacion.route('/api/notificacion', methods=['POST'])
def crear_notificacion():
    return "CREANDO NOTIFICACION"
