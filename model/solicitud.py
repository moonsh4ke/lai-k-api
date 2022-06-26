from db import db

class Solicitud(db.Model):
    numero = db.Column(db.String(10), primary_key=True, nullable=False)
    duenio = db.Column(db.String(10), nullable=False)
    profesional = db.Column(db.String(10), nullable=False)
    fecha = db.Column(db.Date, nullable=True)
    servicio = db.Column(db.String(20), nullable=True)
    direccion = db.Column(db.String(30), nullable=True)
    estado = db.Column(db.String(1), nullable=True)
    comentario = db.Column(db.String(20), nullable=True)