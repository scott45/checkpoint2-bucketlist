import os


def db(current=None):
    if current is None:
        current = 'sqlite'

    dbase = {
        "sqlite": {
            'test': 'sqlite:///testing_db',
            'develop': 'sqlite:///bucketlist_db'
        },

        "postgres": {
            'test': 'postgresql://@localhost/testing_db',
            'develop': 'postgres://pqupzaysfztwij:af1e861efc1bd274966bfe856d378725aa31e4f1205790d70586935bfc8a91ff@ec2-23-21-96-159.compute-1.amazonaws.com:5432/d73kd3chhjbd6p'

        }

    }
    return dbase[current]


class MainConfiguration(object):
    DEBUG = False
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)


class TestingEnvironment(MainConfiguration):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = db()['test']


class DevelopmentEnvironment(MainConfiguration):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = db()['develop']


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
