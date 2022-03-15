import flask
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Document):
    '''This is an ORM that maps data into the table'''
    user_id     = db.IntField(unique=True)
    first_name  = db.StringField(max_length=50)
    last_name   = db.StringField(max_length=50)
    email       = db.StringField(max_length=50, unique=True)
    password    = db.StringField()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password, password)


class Course(db.Document):
    '''This is an ORM that maps data into the table'''
    courseID   =   db.StringField(max_length=10, unique=True)
    title       =   db.StringField(max_length=100)
    description =   db.StringField(max_length=250)
    credits      =   db.IntField()
    term        =   db.StringField(max_length=25)


class Enroll(db.Document):
    '''This is an ORM that maps data into the table'''
    user_id     = db.IntField(unique=True)
    course_id   = db.StringField(max_length=10)
    