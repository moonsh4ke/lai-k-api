import os
from dotenv import load_dotenv

load_dotenv()

class DevelopmentConfig():
    DEBUG = True
    CSRF_SESSION_KEY = "secret"
    SECRET_KEY = 'secret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI')

class ProductionConfig():
    DEBUG = False
    CSRF_SESSION_KEY = "secret"
    SECRET_KEY = 'secret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI')

config = {
        'development': DevelopmentConfig,
        'production': ProductionConfig 
}
