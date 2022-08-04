import os

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'i will find you and i will see your dog/dogs'
    SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS=os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')