from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    xp = db.Column(db.Integer)
    hp =db.Column(db.Integer)
    damage = db.Column(db.Integer)
    armor =db.Column(db.Integer)
    level = db.Column(db.Integer)
    money = db.Column(db.Integer)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Monster(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    xp = db.Column(db.Integer)
    hp =db.Column(db.Integer)
    damage = db.Column(db.Integer)
    armor =db.Column(db.Integer)
    level = db.Column(db.Integer)

class Trader(UserMixin, db.Model):
    username = db.Column(db.String(64), index=True, unique=True)
    itemprice1 = db.Column(db.String(), )
    itemprice2 = db.Column(db.String(), )
    itemprice3 = db.Column(db.String(), )
class Item:
    def __init__(self, name, id, pool, damage, armor, hp, special)
        self.name = name
        self.id = id
        self.pool = pool
        self.damage = damage
        self.armor = armor
        self.special = special

