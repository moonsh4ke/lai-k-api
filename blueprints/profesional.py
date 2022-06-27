from flask import Blueprint, jsonify, request
from model import Usuario, Profesional, Direccion, Servicio, Especialidad, PlanificacionDia, Dia, db
import bcrypt

profesional = Blueprint('profesional', __name__)


@profesional.route('/api/profesionales')
def obtener_profesionales():
    profesionales = Profesional.query.all()
    profesionales = list(map(lambda p: p.to_dict(), profesionales))

    return jsonify(
        {
            'status': 'Ok',
            'message': 'Usuarios obtenidos correctamente',
            'data': profesionales
        }
    ), 200


@profesional.route('/api/profesionales/', methods=['POST'])
def crear_profesional():
    res = request.get_json()
    # Todo: validad schema del json
    old_user = Usuario.query.get(res['rut'])
    if(old_user is None and res):
        hashed_pw = bcrypt.hashpw(
         res['passwrd'].encode('utf-8'), bcrypt.gensalt())

        direccion = Direccion(
         calle=res['direccion']['calle'], numero=res['direccion']['numero'], comuna=res['direccion']['comuna'])

        new_user = Usuario(rut=res['rut'], nombre=res['nombre'], apellidos=res['apellidos'], telefono=res['telefono'],
                        correo=res['correo'], passwrd=hashed_pw, genero=res['genero'], direccion=direccion)

        servicios = []
        for servicio in res['servicios']:
         servicios.append(Servicio.query.get(servicio))


        especialidades = []
        for especialidad in res['especialidades']:
         especialidades.append(Especialidad.query.get(especialidad))

        profesional = Profesional(servicios, especialidades, new_user)

        for dia in res['planificacion'].keys():
            planificacion_dia = PlanificacionDia(inicio=res['planificacion'][dia]['inicio'], fin=res['planificacion'][dia]['fin'])
            planificacion_dia.dia = Dia.query.get(dia)
            with db.session.no_autoflush:
                profesional.planificacion_dias.append(planificacion_dia)
        db.session.add(profesional)
        db.session.commit()

        return jsonify(
            {
                'status': 'OK',
                'message': 'Usuario registrado correctamente'
            }
        )
    return jsonify(
        {
            'status': 'Error',
            'message': 'Usuario ya registrado'
        }
    )
