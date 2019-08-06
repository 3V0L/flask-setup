import os


class Base:
    """Base Class to be inherited by all other classes"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv(
        'SECRET_KEY', '9845465+++RAND000000M=====String!!!!!8726sbajz')
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/flask_api"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Dev(Base):
    """Dev Class with settings for development"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DB')


class Test(Base):
    """Test Class with settings for testing"""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DB')


class Prod(Base):
    """Production Class with settings for production"""
    SQLALCHEMY_DATABASE_URI = os.getenv('PROD_DB')


app_config = {
    'dev': Dev,
    'testing': Test,
    'prod': Prod
}
