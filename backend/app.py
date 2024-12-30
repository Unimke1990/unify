from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


db = SQLAlchemy()

def create_app():
    """
    initializes and configures the flask application
    """
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://agim:1990@localhost/unifydb'
    app.config['SECRET_KEY'] = '1990_stylen9JA'

    #load models
    from models import Users, Contacts, Reminder

    #setting configurations
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_users(uid):
        return Users.query.get(uid)

    #create an instance of bcrypt
    bcrypt = Bcrypt(app)

    #load routes
    # from routes import register_routes
    # register_routes(app, db, bcrypt)

    migrate = Migrate(app, db)

    return app