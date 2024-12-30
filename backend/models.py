from app import db
from flask_login import UserMixin
import bcrypt

class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.string, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True)

    def __init__(self, name, username, password, email):
        self.name = name
        self.username = username
        self.password = self._hash_password(password)
        self.email = email

    def _hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def check_passsword(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password)



class Contacts(db.Model, UserMixin):
    pass

class Reminders(db.Model, UserMixin):
    pass