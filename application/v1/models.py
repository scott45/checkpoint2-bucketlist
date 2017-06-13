from datetime import datetime
from passlib.apps import custom_app_context as pwd_context

from application import databases


class Users(databases.Model):
    __tablename__ = 'User'
    id = databases.Column(databases.Integer, primary_key=True, autoincrement=True)
    Bucket = databases.relationship('BucketList', backref='User')
    username = databases.Column(databases.String(100))
    password_hash = databases.Column(databases.String(200))

    def save(self):
        databases.session.add(self)
        databases.session.commit()

    def hash_password(self, password):
        self.hashed_password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.hashed_password)
