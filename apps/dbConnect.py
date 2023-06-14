from . import config

class ConnectDB(object):
    DATABASE = config.DB_NAME
    USERNAME = config.DB_USER
    PASSWORD = config.DB_PWD
    HOST = config.DB_HOST

    SQLACHEMY_DATABASE_URI = "mysql+pymysql://" + USERNAME + ":" + PASSWORD + "@" + HOST + "/" + DATABASE
    SQLACHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    