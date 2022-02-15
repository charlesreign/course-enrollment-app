import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "f9bf78b9a18ce6d46a0cd2b0b86df9da"