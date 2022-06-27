from flask import Blueprint, jsonify, request
from model import Usuario, Profesional, Servicio, PlanificacionDia, Dia, Solicitud, db
from app import db
import bcrypt

solicitud = Blueprint('solicitud', __name__)

@solicitud.route('/api/solicitud') #METODO GET
def obtener_solicitud():
    return "OBTIENIENDO SOLICITUDES!"

@solicitud.route('/api/solicitud', methods=['POST'])
def crear_solicitud():
    return "CREANDO SOLICITUDES!"