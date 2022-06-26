from db import db

class Notificacion(db.Model):
    idNot = db.Column(db.String(10), primary_key=True, nullable=False)
    emisor = db.Column(db.String(10), nullable=False)
    receptor = db.Column(db.String(10), nullable=False)