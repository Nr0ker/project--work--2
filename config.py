import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'u-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost:3306/project--2'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


