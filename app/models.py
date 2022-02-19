import flask
from app import db



class User(db.Document):
    '''This is an ORM that maps data into the table'''
    user_id     = db.IntField(unique=True)
    first_name  = db.StringField(max_length=50)
    last_name   = db.StringField(max_length=50)
    email       = db.StringField(max_length=50)
    password    = db.StringField(max_length=50)


class Course(db.Document):
    '''This is an ORM that maps data into the table'''
    course_id   =   db.StringField(max_length=10, unique=True)
    title       =   db.StringField(max_length=100)
    description =   db.StringField(max_length=250)
    credit      =   db.IntField()
    term        =   db.StringField(max_length=25)


class Enroll(db.Document):
    '''This is an ORM that maps data into the table'''
    user_id     = db.IntField(unique=True)
    course_id   = db.StringField(max_length=10)
    