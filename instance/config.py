import os


class MainConfiguration(object):
    DEBUG = False
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)


class TestingEnvironment(MainConfiguration):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://@localhost/testing_db'


class DevelopmentEnvironment(MainConfiguration):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://@localhost/bucketlist_db'


class ProductionEnvironment(MainConfiguration):
    DEBUG = False
    TESTING = False


# Dictionary with keys mapping to the different configuration environments
application_configuration = {
    'MainConfiguration': MainConfiguration,
    'TestingEnvironment': TestingEnvironment,
    'DevelopmentEnvironment': DevelopmentEnvironment,
    'ProductionEnvironment': ProductionEnvironment
}
