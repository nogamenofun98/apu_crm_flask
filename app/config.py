import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key'
    DEBUG = True
    CSRF_ENABLED = True
    CAS_URL = "https://cas.apiit.edu.my"
    XML_NAMESPACES = {'cas': 'http://www.yale.edu/tp/cas'}  # add more as needed
    blackListMemberOf = ['CN=All Students,OU=Email Distribution Lists,DC=techlab,DC=apiit,DC=edu,DC=my']
    UPLOADS_DEFAULT_DEST = './app/uploaded/'


class ConfigDB(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/apu_crm'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
