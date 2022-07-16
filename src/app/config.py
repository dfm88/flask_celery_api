
import os

class Config:
    # Secret key for cross site validation
    # randomly generated with python module secrets.token_hex(16)
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')