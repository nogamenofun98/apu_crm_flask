import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key'
    DEBUG = True
    CSRF_ENABLED = True
    CAS_URL = "https://cas.apiit.edu.my"
    XML_NAMESPACES = {'cas': 'http://www.yale.edu/tp/cas'}  # add more as needed


class ConfigDB(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/apu_crm'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
