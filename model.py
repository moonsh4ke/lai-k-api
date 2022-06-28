from app import db

usuario_direccion = db.Table('usuario_direccion',
                             db.Column('usuario.rut', db.String(10), db.ForeignKey(
                                 'usuario.rut'), primary_key=True),
                             db.Column('direccion.id', db.Integer, db.ForeignKey(
                                 'direccion.id'), primary_key=True)
                             )


class Usuario(db.Model):
    rut = db.Column(db.String(10), primary_key=True, nullable=False)
    nombre = db.Column(db.String(30), nullable=False)
    apellidos = db.Column(db.String(30), nullable=False)
    genero = db.Column(db.String(1), nullable=False)
    passwrd = db.Column(db.String(60), nullable=False)
    correo = db.Column(db.String(20), nullable=False)
    telefono = db.Column(db.String(12), nullable=False)

    # Direccion relationship
    direcciones = db.relationship('Direccion', secondary=usuario_direccion, lazy='subquery',
                                  backref=db.backref('usuarios', lazy=True))

    def __init__(self, rut, nombre, apellidos, genero, passwrd, correo, telefono, direccion):
        self.rut = rut
        self.nombre = nombre
        self.apellidos = apellidos
        self.genero = genero
        self.passwrd = passwrd
        self.correo = correo
        self.telefono = telefono
        self.direcciones.append(direccion)

    def __repr__(self):
        return f'Usuario {self.rut} {self.nombre} {self.apellidos}'

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Direccion(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    calle = db.Column(db.String(40), nullable=False)
    comuna = db.Column(db.String(30), db.ForeignKey(
        'comuna.nombre'), nullable=False)
    numero = db.Column(db.Integer, nullable=False)

    # Solicitud relationship
    solicitudes = db.relationship('Solicitud', backref='direccion')

    def __init__(self, calle, comuna, numero):
        self.calle = calle
        self.comuna = comuna
        self.numero = numero


class Comuna(db.Model):
    nombre = db.Column(db.String(30), primary_key=True, nullable=False)

    def __init__(self, nombre):
        self.nombre = nombre


class TipoNotificacion(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    descripcion = db.Column(db.String(30), nullable=False)
    notificaciones = db.relationship('Notificacion', backref='tipo')

    def __init__(self, descripcion):
        self.descripcion = descripcion


class Notificacion(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    estado = db.Column(db.Boolean, nullable=False)
    receptor_rut = db.Column(
        db.String(10), db.ForeignKey('usuario.rut'), nullable=False)
    emisor_rut = db.Column(db.String(10), db.ForeignKey(
        'usuario.rut'), nullable=False)
    tipo_id = db.Column(db.Integer, db.ForeignKey(
        'tipo_notificacion.id'), nullable=False)
    solicitud_id = db.Column(db.Integer, db.ForeignKey(
        'solicitud.id'), nullable=False)

    user_out = db.relationship(
        'Usuario', backref='notificaciones_out', foreign_keys=[emisor_rut])
    user_in = db.relationship(
        'Usuario', backref='notificaciones_in', foreign_keys=[receptor_rut])

    def __init__(self, receptor_rut, emisor_rut, tipo_id, solicitud_id):
        self.receptor_rut = receptor_rut
        self.emisor_rut = emisor_rut
        self.tipo_id = tipo_id
        self.solicitud_id = solicitud_id


especialidad_profesional = db.Table('especialidad_profesional',
                                    db.Column('especialidad_nombre', db.String(30), db.ForeignKey(
                                        'especialidad.nombre'), primary_key=True),
                                    db.Column('profesional_rut', db.String(10), db.ForeignKey(
                                        'profesional.rut'), primary_key=True)
                                    )

servicio_profesional = db.Table('servicio_profesional',
                                db.Column('servicio_nombre', db.String(30), db.ForeignKey(
                                    'servicio.nombre'), primary_key=True),
                                db.Column('profesional_rut', db.String(10), db.ForeignKey(
                                    'profesional.rut'), primary_key=True)
                                )


class Duenio(db.Model):
    rut = db.Column(db.String(10), db.ForeignKey(
        'usuario.rut'), primary_key=True, nullable=False)

    # Solicitud relationship
    solicitudes = db.relationship('Solicitud', backref='duenio')

    usuario = db.relationship('Usuario', backref='duenio', uselist=False)

    def __init__(self, usuario):
        self.usuario = usuario

    def to_dict(self):
        return {"nombre": self.usuario.nombre, "apellidos": self.usuario.apellidos, "rut": self.rut}


class Profesional(db.Model):
    rut = db.Column(db.String(10), db.ForeignKey(
        'usuario.rut'), primary_key=True, nullable=False)

    # Especialidad relationship
    especialidades = db.relationship('Especialidad', secondary=especialidad_profesional, lazy='subquery',
                                     backref=db.backref('profesionales', lazy=True))

    # Servicio relationship
    servicios = db.relationship('Servicio', secondary=servicio_profesional, lazy='subquery',
                                backref=db.backref('profesionales', lazy=True))

    # Dia relationship
    planificacion_dias = db.relationship(
        'PlanificacionDia', back_populates='profesional')

    # Solicitud relationship
    solicitudes = db.relationship('Solicitud', backref='profesional')

    usuario = db.relationship('Usuario', backref='profesional', uselist=False)

    def __init__(self, servicios, especialidades, usuario):
        self.servicios = servicios
        self.especialidades = especialidades
        self.usuario = usuario

    def to_dict(self):
        return {"nombre": self.usuario.nombre, "apellidos": self.usuario.apellidos, "rut": self.rut, "servicios": list(map(lambda s: s.nombre, self.servicios)), "especialidades": list(map(lambda e: e.nombre, self.especialidades))}


class Dia(db.Model):
    nombre = db.Column(db.String(10), nullable=False, primary_key=True)
    profesionales = db.relationship('PlanificacionDia', back_populates='dia')

    def __init__(self, nombre):
        self.nombre = nombre


class PlanificacionDia(db.Model):
    profesional_rut = db.Column(db.String(10), db.ForeignKey(
        'profesional.rut'), primary_key=True)
    dia_nombre = db.Column(db.String(10), db.ForeignKey(
        'dia.nombre'), primary_key=True)
    inicio = db.Column(db.String(10), nullable=True)
    fin = db.Column(db.String(10), nullable=True)
    dia = db.relationship('Dia', back_populates='profesionales')
    profesional = db.relationship(
        'Profesional', back_populates='planificacion_dias')

    def __init__(self, inicio, fin):
        self.inicio = inicio
        self.fin = fin


class Especialidad(db.Model):
    nombre = db.Column(db.String(30), nullable=False, primary_key=True)
    descipcion = db.Column(db.String(500), nullable=False)

    def __init__(self, nombre, descipcion):
        self.nombre = nombre
        self.descipcion = descipcion


class Servicio(db.Model):
    nombre = db.Column(db.String(30), nullable=False, primary_key=True)
    descipcion = db.Column(db.String(40), nullable=False)

    def __init__(self, nombre, descipcion):
        self.nombre = nombre
        self.descipcion = descipcion


class EstadoVisita(db.Model):
    nombre = db.Column(db.String(30), nullable=False, primary_key=True)
    descipcion = db.Column(db.String(30), nullable=False)
    visitas = db.relationship('Visita', backref='estado')

    def __init__(self, nombre, descipcion):
        self.nombre = nombre
        self.descipcion = descipcion


class Visita(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    estado_nombre = db.Column(db.String(30), db.ForeignKey(
        'estado_visita.nombre'), nullable=False)
    solicitud_id = db.Column(db.Integer, db.ForeignKey(
        'solicitud.id'), nullable=False)

    def __init__(self, estado_nombre, solicitud_id):
        self.estado_nombre = estado_nombre
        self.solicitud_id = solicitud_id


class Solicitud(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    profesional_rut = db.Column(db.String(10), db.ForeignKey(
        'profesional.rut'), nullable=False)
    duenio_rut = db.Column(db.String(10), db.ForeignKey(
        'duenio.rut'), nullable=False)
    direccion_id = db.Column(db.Integer, db.ForeignKey(
        'direccion.id'), nullable=False)
    estado_nombre = db.Column(db.String(30), db.ForeignKey(
        'estado_solicitud.nombre'), nullable=False)
    comentario = db.Column(db.String(100), nullable=True)

    servicio_nombre = db.Column(db.String(30), db.ForeignKey(
        'servicio.nombre'), nullable=False)

    servicio = db.relationship('Servicio', backref='solicitudes')

    fecha_hora = db.Column(db.DateTime, nullable=False)

    def __init__(self, profesional_rut, duenio_rut, direccion_id, estado_nombre, comentario):
        self.profesional_rut = profesional_rut
        self.duenio_rut = duenio_rut
        self.direccion_id = direccion_id
        self.estado_nombre = estado_nombre
        self.comentario = comentario


class EstadoSolicitud(db.Model):
    nombre = db.Column(db.String(30), nullable=False, primary_key=True)
    descipcion = db.Column(db.String(30), nullable=False)
    solicitudes = db.relationship('Solicitud', backref='estado')

    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descipcion = descripcion


# db.session.add(Comuna("Arica"))
# db.session.add(Comuna("Camarones"))
# db.session.add(Comuna("General Lagos"))
# db.session.add(Comuna("Putre"))
# db.session.add(Comuna("Alto Hospicio"))
# db.session.add(Comuna("Iquique"))
# db.session.add(Comuna("Camiña"))
# db.session.add(Comuna("Colchane"))
# db.session.add(Comuna("Huara"))
# db.session.add(Comuna("Pica"))
# db.session.add(Comuna("Pozo Almonte"))
# db.session.add(Comuna("Antofagasta"))
# db.session.add(Comuna("Mejillones"))
# db.session.add(Comuna("Sierra Gorda"))
# db.session.add(Comuna("Taltal"))
# db.session.add(Comuna("Calama"))
# db.session.add(Comuna("Ollague"))
# db.session.add(Comuna("San Pedro de Atacama"))
# db.session.add(Comuna("María Elena"))
# db.session.add(Comuna("Tocopilla"))
# db.session.add(Comuna("Chañaral"))
# db.session.add(Comuna("Diego de Almagro"))
# db.session.add(Comuna("Caldera"))
# db.session.add(Comuna("Copiapó"))
# db.session.add(Comuna("Tierra Amarilla"))
# db.session.add(Comuna("Alto del Carmen"))
# db.session.add(Comuna("Freirina"))
# db.session.add(Comuna("Huasco"))
# db.session.add(Comuna("Vallenar"))
# db.session.add(Comuna("Canela"))
# db.session.add(Comuna("Illapel"))
# db.session.add(Comuna("Los Vilos"))
# db.session.add(Comuna("Salamanca"))
# db.session.add(Comuna("Andacollo"))
# db.session.add(Comuna("Coquimbo"))
# db.session.add(Comuna("La Higuera"))
# db.session.add(Comuna("La Serena"))
# db.session.add(Comuna("Paihuaco"))
# db.session.add(Comuna("Vicuña"))
# db.session.add(Comuna("Combarbalá"))
# db.session.add(Comuna("Monte Patria"))
# db.session.add(Comuna("Ovalle"))
# db.session.add(Comuna("Punitaqui"))
# db.session.add(Comuna("Río Hurtado"))
# db.session.add(Comuna("Isla de Pascua"))
# db.session.add(Comuna("Calle Larga"))
# db.session.add(Comuna("Los Andes"))
# db.session.add(Comuna("Rinconada"))
# db.session.add(Comuna("San Esteban"))
# db.session.add(Comuna("La Ligua"))
# db.session.add(Comuna("Papudo"))
# db.session.add(Comuna("Petorca"))
# db.session.add(Comuna("Zapallar"))
# db.session.add(Comuna("Hijuelas"))
# db.session.add(Comuna("La Calera"))
# db.session.add(Comuna("La Cruz"))
# db.session.add(Comuna("Limache"))
# db.session.add(Comuna("Nogales"))
# db.session.add(Comuna("Olmué"))
# db.session.add(Comuna("Quillota"))
# db.session.add(Comuna("Algarrobo"))
# db.session.add(Comuna("Cartagena"))
# db.session.add(Comuna("El Quisco"))
# db.session.add(Comuna("El Tabo"))
# db.session.add(Comuna("San Antonio"))
# db.session.add(Comuna("Santo Domingo"))
# db.session.add(Comuna("Catemu"))
# db.session.add(Comuna("Llaillay"))
# db.session.add(Comuna("Panquehue"))
# db.session.add(Comuna("Putaendo"))
# db.session.add(Comuna("San Felipe"))
# db.session.add(Comuna("Santa María"))
# db.session.add(Comuna("Casablanca"))
# db.session.add(Comuna("Concón"))
# db.session.add(Comuna("Juan Fernández"))
# db.session.add(Comuna("Puchuncaví"))
# db.session.add(Comuna("Quilpué"))
# db.session.add(Comuna("Quintero"))
# db.session.add(Comuna("Valparaíso"))
# db.session.add(Comuna("Villa Alemana"))
# db.session.add(Comuna("Viña del Mar"))
# db.session.add(Comuna("Colina"))
# db.session.add(Comuna("Lampa"))
# db.session.add(Comuna("Tiltil"))
# db.session.add(Comuna("Pirque"))
# db.session.add(Comuna("Puente Alto"))
# db.session.add(Comuna("San José de Maipo"))
# db.session.add(Comuna("Buin"))
# db.session.add(Comuna("Calera de Tango"))
# db.session.add(Comuna("Paine"))
# db.session.add(Comuna("San Bernardo"))
# db.session.add(Comuna("Alhué"))
# db.session.add(Comuna("Curacaví"))
# db.session.add(Comuna("María Pinto"))
# db.session.add(Comuna("Melipilla"))
# db.session.add(Comuna("San Pedro"))
# db.session.add(Comuna("Cerrillos"))
# db.session.add(Comuna("Cerro Navia"))
# db.session.add(Comuna("Conchalí"))
# db.session.add(Comuna("El Bosque"))
# db.session.add(Comuna("Estación Central"))
# db.session.add(Comuna("Huechuraba"))
# db.session.add(Comuna("Independencia"))
# db.session.add(Comuna("La Cisterna"))
# db.session.add(Comuna("La Granja"))
# db.session.add(Comuna("La Florida"))
# db.session.add(Comuna("La Pintana"))
# db.session.add(Comuna("La Reina"))
# db.session.add(Comuna("Las Condes"))
# db.session.add(Comuna("Lo Barnechea"))
# db.session.add(Comuna("Lo Espejo"))
# db.session.add(Comuna("Lo Prado"))
# db.session.add(Comuna("Macul"))
# db.session.add(Comuna("Maipú"))
# db.session.add(Comuna("Ñuñoa"))
# db.session.add(Comuna("Pedro Aguirre Cerda"))
# db.session.add(Comuna("Peñalolén"))
# db.session.add(Comuna("Providencia"))
# db.session.add(Comuna("Pudahuel"))
# db.session.add(Comuna("Quilicura"))
# db.session.add(Comuna("Quinta Normal"))
# db.session.add(Comuna("Recoleta"))
# db.session.add(Comuna("Renca"))
# db.session.add(Comuna("San Miguel"))
# db.session.add(Comuna("San Joaquín"))
# db.session.add(Comuna("San Ramón"))
# db.session.add(Comuna("Santiago"))
# db.session.add(Comuna("Vitacura"))
# db.session.add(Comuna("El Monte"))
# db.session.add(Comuna("Isla de Maipo"))
# db.session.add(Comuna("Padre Hurtado"))
# db.session.add(Comuna("Peñaflor"))
# db.session.add(Comuna("Talagante"))
# db.session.add(Comuna("Codegua"))
# db.session.add(Comuna("Coínco"))
# db.session.add(Comuna("Coltauco"))
# db.session.add(Comuna("Doñihue"))
# db.session.add(Comuna("Graneros"))
# db.session.add(Comuna("Las Cabras"))
# db.session.add(Comuna("Machalí"))
# db.session.add(Comuna("Malloa"))
# db.session.add(Comuna("Mostazal"))
# db.session.add(Comuna("Olivar"))
# db.session.add(Comuna("Peumo"))
# db.session.add(Comuna("Pichidegua"))
# db.session.add(Comuna("Quinta de Tilcoco"))
# db.session.add(Comuna("Rancagua"))
# db.session.add(Comuna("Rengo"))
# db.session.add(Comuna("Requínoa"))
# db.session.add(Comuna("San Vicente de Tagua Tagua"))
# db.session.add(Comuna("La Estrella"))
# db.session.add(Comuna("Litueche"))
# db.session.add(Comuna("Marchihue"))
# db.session.add(Comuna("Navidad"))
# db.session.add(Comuna("Peredones"))
# db.session.add(Comuna("Pichilemu"))
# db.session.add(Comuna("Chépica"))
# db.session.add(Comuna("Chimbarongo"))
# db.session.add(Comuna("Lolol"))
# db.session.add(Comuna("Nancagua"))
# db.session.add(Comuna("Palmilla"))
# db.session.add(Comuna("Peralillo"))
# db.session.add(Comuna("Placilla"))
# db.session.add(Comuna("Pumanque"))
# db.session.add(Comuna("San Fernando"))
# db.session.add(Comuna("Santa Cruz"))
# db.session.add(Comuna("Cauquenes"))
# db.session.add(Comuna("Chanco"))
# db.session.add(Comuna("Pelluhue"))
# db.session.add(Comuna("Curicó"))
# db.session.add(Comuna("Hualañé"))
# db.session.add(Comuna("Licantén"))
# db.session.add(Comuna("Molina"))
# db.session.add(Comuna("Rauco"))
# db.session.add(Comuna("Romeral"))
# db.session.add(Comuna("Sagrada Familia"))
# db.session.add(Comuna("Teno"))
# db.session.add(Comuna("Vichuquén"))
# db.session.add(Comuna("Colbún"))
# db.session.add(Comuna("Linares"))
# db.session.add(Comuna("Longaví"))
# db.session.add(Comuna("Parral"))
# db.session.add(Comuna("Retiro"))
# db.session.add(Comuna("San Javier"))
# db.session.add(Comuna("Villa Alegre"))
# db.session.add(Comuna("Yerbas Buenas"))
# db.session.add(Comuna("Constitución"))
# db.session.add(Comuna("Curepto"))
# db.session.add(Comuna("Empedrado"))
# db.session.add(Comuna("Maule"))
# db.session.add(Comuna("Pelarco"))
# db.session.add(Comuna("Pencahue"))
# db.session.add(Comuna("Río Claro"))
# db.session.add(Comuna("San Clemente"))
# db.session.add(Comuna("San Rafael"))
# db.session.add(Comuna("Talca"))
# db.session.add(Comuna("Arauco"))
# db.session.add(Comuna("Cañete"))
# db.session.add(Comuna("Contulmo"))
# db.session.add(Comuna("Curanilahue"))
# db.session.add(Comuna("Lebu"))
# db.session.add(Comuna("Los Álamos"))
# db.session.add(Comuna("Tirúa"))
# db.session.add(Comuna("Alto Biobío"))
# db.session.add(Comuna("Antuco"))
# db.session.add(Comuna("Cabrero"))
# db.session.add(Comuna("Laja"))
# db.session.add(Comuna("Los Ángeles"))
# db.session.add(Comuna("Mulchén"))
# db.session.add(Comuna("Nacimiento"))
# db.session.add(Comuna("Negrete"))
# db.session.add(Comuna("Quilaco"))
# db.session.add(Comuna("Quilleco"))
# db.session.add(Comuna("San Rosendo"))
# db.session.add(Comuna("Santa Bárbara"))
# db.session.add(Comuna("Tucapel"))
# db.session.add(Comuna("Yumbel"))
# db.session.add(Comuna("Chiguayante"))
# db.session.add(Comuna("Concepción"))
# db.session.add(Comuna("Coronel"))
# db.session.add(Comuna("Florida"))
# db.session.add(Comuna("Hualpén"))
# db.session.add(Comuna("Hualqui"))
# db.session.add(Comuna("Lota"))
# db.session.add(Comuna("Penco"))
# db.session.add(Comuna("San Pedro de La Paz"))
# db.session.add(Comuna("Santa Juana"))
# db.session.add(Comuna("Talcahuano"))
# db.session.add(Comuna("Tomé"))
# db.session.add(Comuna("Bulnes"))
# db.session.add(Comuna("Chillán"))
# db.session.add(Comuna("Chillán Viejo"))
# db.session.add(Comuna("Cobquecura"))
# db.session.add(Comuna("Coelemu"))
# db.session.add(Comuna("Coihueco"))
# db.session.add(Comuna("El Carmen"))
# db.session.add(Comuna("Ninhue"))
# db.session.add(Comuna("Ñiquen"))
# db.session.add(Comuna("Pemuco"))
# db.session.add(Comuna("Pinto"))
# db.session.add(Comuna("Portezuelo"))
# db.session.add(Comuna("Quillón"))
# db.session.add(Comuna("Quirihue"))
# db.session.add(Comuna("Ránquil"))
# db.session.add(Comuna("San Carlos"))
# db.session.add(Comuna("San Fabián"))
# db.session.add(Comuna("San Ignacio"))
# db.session.add(Comuna("San Nicolás"))
# db.session.add(Comuna("Treguaco"))
# db.session.add(Comuna("Yungay"))
# db.session.add(Comuna("Carahue"))
# db.session.add(Comuna("Cholchol"))
# db.session.add(Comuna("Cunco"))
# db.session.add(Comuna("Curarrehue"))
# db.session.add(Comuna("Freire"))
# db.session.add(Comuna("Galvarino"))
# db.session.add(Comuna("Gorbea"))
# db.session.add(Comuna("Lautaro"))
# db.session.add(Comuna("Loncoche"))
# db.session.add(Comuna("Melipeuco"))
# db.session.add(Comuna("Nueva Imperial"))
# db.session.add(Comuna("Padre Las Casas"))
# db.session.add(Comuna("Perquenco"))
# db.session.add(Comuna("Pitrufquén"))
# db.session.add(Comuna("Pucón"))
# db.session.add(Comuna("Saavedra"))
# db.session.add(Comuna("Temuco"))
# db.session.add(Comuna("Teodoro Schmidt"))
# db.session.add(Comuna("Toltén"))
# db.session.add(Comuna("Vilcún"))
# db.session.add(Comuna("Villarrica"))
# db.session.add(Comuna("Angol"))
# db.session.add(Comuna("Collipulli"))
# db.session.add(Comuna("Curacautín"))
# db.session.add(Comuna("Ercilla"))
# db.session.add(Comuna("Lonquimay"))
# db.session.add(Comuna("Los Sauces"))
# db.session.add(Comuna("Lumaco"))
# db.session.add(Comuna("Purén"))
# db.session.add(Comuna("Renaico"))
# db.session.add(Comuna("Traiguén"))
# db.session.add(Comuna("Victoria"))
# db.session.add(Comuna("Corral"))
# db.session.add(Comuna("Lanco"))
# db.session.add(Comuna("Los Lagos"))
# db.session.add(Comuna("Máfil"))
# db.session.add(Comuna("Mariquina"))
# db.session.add(Comuna("Paillaco"))
# db.session.add(Comuna("Panguipulli"))
# db.session.add(Comuna("Valdivia"))
# db.session.add(Comuna("Futrono"))
# db.session.add(Comuna("La Unión"))
# db.session.add(Comuna("Lago Ranco"))
# db.session.add(Comuna("Río Bueno"))
# db.session.add(Comuna("Ancud"))
# db.session.add(Comuna("Castro"))
# db.session.add(Comuna("Chonchi"))
# db.session.add(Comuna("Curaco de Vélez"))
# db.session.add(Comuna("Dalcahue"))
# db.session.add(Comuna("Puqueldón"))
# db.session.add(Comuna("Queilén"))
# db.session.add(Comuna("Quemchi"))
# db.session.add(Comuna("Quellón"))
# db.session.add(Comuna("Quinchao"))
# db.session.add(Comuna("Calbuco"))
# db.session.add(Comuna("Cochamó"))
# db.session.add(Comuna("Fresia"))
# db.session.add(Comuna("Frutillar"))
# db.session.add(Comuna("Llanquihue"))
# db.session.add(Comuna("Los Muermos"))
# db.session.add(Comuna("Maullín"))
# db.session.add(Comuna("Puerto Montt"))
# db.session.add(Comuna("Puerto Varas"))
# db.session.add(Comuna("Osorno"))
# db.session.add(Comuna("Puero Octay"))
# db.session.add(Comuna("Purranque"))
# db.session.add(Comuna("Puyehue"))
# db.session.add(Comuna("Río Negro"))
# db.session.add(Comuna("San Juan de la Costa"))
# db.session.add(Comuna("San Pablo"))
# db.session.add(Comuna("Chaitén"))
# db.session.add(Comuna("Futaleufú"))
# db.session.add(Comuna("Hualaihué"))
# db.session.add(Comuna("Palena"))
# db.session.add(Comuna("Aisén"))
# db.session.add(Comuna("Cisnes"))
# db.session.add(Comuna("Guaitecas"))
# db.session.add(Comuna("Cochrane"))
# db.session.add(Comuna("O\'higgins"))
# db.session.add(Comuna("Tortel"))
# db.session.add(Comuna("Coihaique"))
# db.session.add(Comuna("Lago Verde"))
# db.session.add(Comuna("Chile Chico"))
# db.session.add(Comuna("Río Ibáñez"))
# db.session.add(Comuna("Antártica"))
# db.session.add(Comuna("Cabo de Hornos"))
# db.session.add(Comuna("Laguna Blanca"))
# db.session.add(Comuna("Punta Arenas"))
# db.session.add(Comuna("Río Verde"))
# db.session.add(Comuna("San Gregorio"))
# db.session.add(Comuna("Porvenir"))
# db.session.add(Comuna("Primavera"))
# db.session.add(Comuna("Timaukel"))
# db.session.add(Comuna("Natales"))
# db.session.add(Comuna("Torres del Paine"))


# db.session.add(Dia("Lunes"))
# db.session.add(Dia("Martes"))
# db.session.add(Dia("Miercoles"))
# db.session.add(Dia("Jueves"))
# db.session.add(Dia("Viernes"))
# db.session.add(Dia("Sabado"))
# db.session.add(Dia("Domingo"))

# db.session.commit()
