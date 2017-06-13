import os


class MainConfiguration(object):
    pass


class TestingEnvironment(MainConfiguration):
    DEBUG = True
    TESTING = True


class DevelopmentEnvironment(MainConfiguration):
    DEBUG = True
    TESTING = True


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
