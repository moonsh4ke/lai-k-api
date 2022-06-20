from crypt import methods
import re
from flask import Flask, send_from_directory
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from requests import request #comentar en despliegue
from flask_mysqldb import MySQL

#Objetos
from Entity import Usuario


#Flask config
app = Flask(__name__,static_url_path='',static_folder='frontend/build')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'lai_k'

mysql = MySQL(app)


@app.route("/registro",methods=["POST"],strict_slashes=False)
def registrar_usuario():
    usuario = Usuario(
        request.json['nombres'],
        request.json['apellidos'],
        request.json['comuna'],
        request.json['calle'],
        request.json['numero'],
        request.json['telefono'],
        request.json['email'],
        request.json['tipo_usuario']
    )
    INSERT(usuario)


def INSERT(usuario:Usuario):
    cursor = mysql.connection.cursor()
    cursor.execute(
        '''INSERT INTO USUARIO VALUES(%s,%s,%i,%s,%s,%s,%s)''',
        (   usuario.nombres,
            usuario.apellidos,
            usuario.comuna,
            usuario.calle,
            usuario.numero,
            usuario.telefono,
            usuario.email,
            usuario.tipo_usuario)
        )
    mysql.connection.commit()
    cursor.close()