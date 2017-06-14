from datetime import datetime
from passlib.apps import custom_app_context as pwd_context

from app import databases


class Users(databases.Model):
    __tablename__ = 'User'
    id = databases.Column(databases.Integer, primary_key=True, autoincrement=True)
    Bucket = databases.relationship('BucketList', backref='User')
    username = databases.Column(databases.String(100))
    new_password = databases.Column(databases.String(200))

    def save(self):
        databases.session.add(self)
        databases.session.commit()

    def hash_password(self, password):
        self.new_password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.new_password)


class BucketList(databases.Model):
    __tablename__ = 'Bucketlist'
    id = databases.Column(databases.Integer, primary_key=True, autoincrement=True)
    user = databases.Column(databases.Integer, databases.ForeignKey('User.id'))
    name = databases.Column(databases.Strinag(150))
    date_created = databases.Column(databases.DateTime, default=datetime.utcnow())
    date_modified = databases.Column(databases.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())
    created_by = databases.Column(databases.Integer())

    def __init__(self, name, created_by):
        self.name = name
        self.created_by = created_by

    def save(self):
        databases.session.add(self)
        databases.session.commit()


class Items(databases.Model):
    __tablename__ = 'BucketlistItems'
    id = databases.Column(databases.Integer, primary_key=True, autoincrement=True)
    name = databases.Column(databases.String(200))
    date_created = databases.Column(databases.DateTime, default=datetime.utcnow())
    date_modified = databases.Column(databases.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())
    bucketlist_id = databases.Column(databases.Integer, databases.ForeignKey('Bucketlist.id'))

    def __init__(self, name, bucketlist_id):
        self.name = name
        self.bucketlist_id = bucketlist_id

    def save(self):
        databases.session.add(self)
        databases.session.commit()

    def __repr__(self):
        return '<Items {}'.format(self.name)
