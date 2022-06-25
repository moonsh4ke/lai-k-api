from db import db

class Usuario(db.Model):
    rut = db.Column(db.String(10), primary_key=True, nullable=True)
    nombre = db.Column(db.String(30), nullable=True)
    apellidos = db.Column(db.String(30), nullable=True)
    genero = db.Column(db.String(1), nullable=True)
    passwrd = db.Column(db.String(60), nullable=True)
    direccion = db.Column(db.String(20), nullable=True)
    correo = db.Column(db.String(20), nullable=True)
    telefono = db.Column(db.String(12), nullable=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def to_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}