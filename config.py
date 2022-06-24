# Objeto de configuracion de la app de Flask
class DevelopmentConfig():
    DEBUG = True
    MYSQL_HOST = 'lai-k.cazjtw8hhb0a.us-east-1.rds.amazonaws.com'
    MYSQL_PASSWORD = 'JFx9S7Tjlf8ehMnOV91d'
    MYSQL_DB = 'lai-k'
    SECRET_KEY = ''

config = {
        'development' : DevelopmentConfig
}
