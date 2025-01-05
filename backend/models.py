from app import db
from flask_login import UserMixin
import bcrypt

class Users(db.Model, UserMixin):
    """
    The Users class represents the users table.
    """
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(250), unique=True)

    #initialize new users
    def __init__(self, name, username, password, email):
        self.name = name
        self.username = username
        self.password = self._hash_password(password)
        self.email = email

    #hash entered password
    def _hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    #compare provided password with stored hashed password
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
    #user representation
    def __repr__(self):
        return f"User(name={self.name}, username={self.username})"

    #retrieve users uid
    def get_id(self):
        return self.uid


#groups table
class Group(db.Model):
    """
    The Group class represents the groups table.
    """
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)
    contacts = db.relationship('Contacts', secondary='contact_groups', backref=db.backref('groups', lazy=True))

    def __init__(self, name, user_id):
        """
        Initialize a new Group instance.
        """
        self.name = name
        self.user_id = user_id


class Contacts(db.Model):
    """
    The Contacts class represents the contacts table.
    """
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False) 
    user = db.relationship('Users', backref=db.backref('contacts', lazy=True))

    #initialize new users
    def __init__(self, name, email, phone, user_id):
        self.name = name
        self.email =email
        self.phone = phone
        self.user_id = user_id


contact_groups = db.Table('contact_groups',
    db.Column('contact_id', db.Integer, db.ForeignKey('contacts.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'), primary_key=True)
)


class Reminder(db.Model):
    """
     The Reminder class represents the reminders table.
    """
    __tablename__ = 'reminders'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)
    user = db.relationship('Users', backref=db.backref('reminders', lazy=True))

    def __init__(self, title, description, due_date, user_id):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.user_id = user_id
