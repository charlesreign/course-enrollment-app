import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'D\xb1\x9a\xe5{\xecS\xea\xdfZ\xd9\xe9o\xbf4\x95'

    MONGODB_SETTINGS = {'db': 'Enrollment',
    'host': 'mongodb://localhost:27017/Enrollment'
    }