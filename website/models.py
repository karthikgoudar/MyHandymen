from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import LargeBinary


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150))
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))



class Role(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))


class HandymanProfessionCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100)) 


class HandymanInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname1 = db.Column(db.String(150))
    lastname1 = db.Column(db.String(150))
    email1 = db.Column(db.String(150), unique=True)
    professioncategory = db.Column(db.String(100))
    gender = db.Column(db.String(50))
    phone = db.Column(db.Integer)
    price_per_hour = db.Column(db.Integer)
    description = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    profileimage = db.Column(db.LargeBinary)
    
