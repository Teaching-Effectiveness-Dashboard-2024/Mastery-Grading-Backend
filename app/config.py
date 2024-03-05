import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.dirname(basedir)
load_dotenv(os.path.join(parent_dir, '.env'))


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
