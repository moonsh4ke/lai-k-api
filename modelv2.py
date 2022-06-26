from db import db

class Usuario(db.Model):
    rut = db.Column(db.String(10), primary_key=True, nullable=False)
    nombre = db.Column(db.String(30), nullable=False)
    apellidos = db.Column(db.String(30), nullable=False)
    genero = db.Column(db.String(1), nullable=False)
    passwrd = db.Column(db.String(60), nullable=False)
    region_num = db.Column(db.String(40), db.ForeignKey('region.num'), nullable=False)
    comuna_id = db.Column(db.String(40), db.ForeignKey('comuna.id'), nullable=False)
    direccion = db.Column(db.String(20), nullable=False)
    correo = db.Column(db.String(20), nullable=False)
    telefono = db.Column(db.String(12), nullable=False)

    # Notificacion relationship
    notificaciones_out = db.relationship('Notificacion', backref='emisor')
    notificaciones_in = db.relationship('Notificacion', backref='receptor')

    def __repr__(self):
        return f'Usuario {self.rut} {self.nombre} {self.apellidos}'

    def to_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Region(db.Model):
    num = db.Column(db.Integer, primary_key=True, nullable=False)
    nombre = db.Column(db.String(40), nullable=False)
    usuarios = db.relationship('Usuario', backref='region')

class Comuna(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nombre = db.Column(db.String(40), nullable=False)
    usuarios = db.relationship('Usuario', backref='comuna')

class TipoNotificacion(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    descripcion = db.Column(db.String(30), nullable=False)
    notificaciones = db.relationship('Notificacion', backref='tipo')

class Notificacion(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    Estado = db.Column(db.Boolean, nullable=False)
    receptor_rut = db.Column(db.String(10), db.ForeignKey('usuario.rut'), nullable=False)
    emisor_rut = db.Column(db.String(10), db.ForeignKey('usuario.rut'), nullable=False)
    tipo_id = db.Column(db.Integer, db.ForeignKey('tipo_notificacion.id'), nullable=False)
    solicitud_id = db.Column(db.Integer, db.ForeignKey('solicitud.id'), nullable=False)

especialidad_profesional = db.Table('especialidad_profesional',
    db.Column('especialidad_id', db.Integer, db.ForeignKey('especialidad.id'), primary_key=True),
    db.Column('profesional_rut', db.String(10), db.ForeignKey('profesional.rut'), primary_key=True)
)

servicio_profesional = db.Table('servicio_profesional',
    db.Column('servicio_id', db.Integer, db.ForeignKey('servicio.id'), primary_key=True),
    db.Column('profesional_rut', db.String(10), db.ForeignKey('profesional.rut'), primary_key=True)
)

planificacion_dia = db.Table('planificacion_dia',
    db.Column('profesional_rut', db.String(10), db.ForeignKey('profesional.rut'), primary_key=True),
    db.Column('dia_id', db.Integer, db.ForeignKey('dia.id'), primary_key=True),
    inicio = db.Column(db.DateTime, nullable=False),
    fin = db.Column(db.DateTime, nullable=False)
)

class Profesional(db.Model):
    rut = db.Column(db.String(10), db.ForeignKey('usuario.rut'), primary_key=True, nullable=False)

    # Especialidad relationship
    especialidades = db.relationship('Especialidad', secondary=especialidad_profesional, lazy='subquery',
    backref=db.backref('profesionales', lazy=True))

    # Servicio relationship
    servicios = db.relationship('Servicio', secondary=servicio_profesional, lazy='subquery',
    backref=db.backref('profesionales', lazy=True))

    # Dia relationship
    planificacion_dias = db.relationship('Dia', secondary=planificacion_dia, lazy='subquery',
    backref=db.backref('profesionales', lazy=True))

class Dia(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nombre = db.Column(10)

class Especialidad(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nombre = db.Column(db.String(30), nullable=False)
    descipcion = db.Column(db.String(40), nullable=False)

class Servicio(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nombre = db.Column(db.String(30), nullable=False)
    descipcion = db.Column(db.String(40), nullable=False)

class EstadoVisita(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nombre = db.Column(db.String(20), nullable=False)
    descipcion = db.Column(db.String(30), nullable=False)
    visitas = db.relationship('Visita', backref='estado_visita')

class Visita(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    estado_id = db.Column(db.Integer, db.ForeignKey('estado_visita.id'), nullable=False)
    solicitud_id = db.Column(db.Integer, db.ForeignKey('solicitud.id'), nullable=False)

class Solicitud(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    profesional_rut = db.Column(db.String(10), db.ForeignKey('profesional.rut'), nullable=False)
    duenio= db.Column(db.String(10), db.ForeignKey('usuario.rut'), nullable=False)
    region_num = db.Column(db.String(40), db.ForeignKey('region.num'), nullable=False)
    comuna_id = db.Column(db.String(40), db.ForeignKey('comuna.id'), nullable=False)
    direccion = db.Column(db.String(20), nullable=False)
    estado_id = db.Column(db.Integer, db.ForeignKey('estado_solicitud.id'), nullable=False)
    comentario = db.Column(db.String(100), nullable=True)

class EstadoSolicitud(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nombre = db.Column(db.String(20), nullable=False)
    descipcion = db.Column(db.String(30), nullable=False)
    solicitudes = db.relationship('Solicitud', backref='estado_solicitud')
