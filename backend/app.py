from flask import Flask, url_for, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from datetime import timedelta
from flask import session


db = SQLAlchemy()

def create_app():
    """
    initializes and configures the flask application
    """
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://agim:1990@localhost/unifydb'
    app.config['SECRET_KEY'] = '1990_stylen9JA'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

    @app.before_request
    def refresh_session():
        session.modified = True
        if 'user_id' not in session and (request.endpoint is None or request.endpoint not in ['login', 'register']):
            flash('Your session has expired. Please log in again.')
            return redirect(url_for('login'))

    #load models
    from models import Users, Contacts, Reminder

    #setting configurations
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_users(uid):
        user = Users.query.get(uid)
        return user if user else None
    
    #login required manager for update_profile, and delete_profile
    @login_manager.unauthorized_handler
    def unauthorized():
        # Determine which route triggered the unauthorized request
        if request.path == url_for('update_profile'):
            flash('You must be logged in before you can update your profile')
            return redirect(url_for('login'))

        elif request.path == url_for('delete_account'):
            flash('You must be logged in before you can delete your account')
            return redirect(url_for('login'))

        elif request.path == url_for('add_contact'):
            flash('You must be logged in before you can add a contact')
            return redirect(url_for('login'))

        elif request.path == url_for('contacts'):
            flash('You must be logged in before you can view your contacts')
            return redirect(url_for('login'))
        
        elif request.path == url_for('edit_contact'):
            flash('You must be logged in before you can edit your contacts')
            return redirect(url_for('login'))
        
        elif request.path == url_for('delete_contact'):
            flash('You must be logged in before you can delete your contacts')
            return redirect(url_for('login'))

        else:
            flash('You must be logged in to access this page')
            return redirect(url_for('login'))
    

    #create an instance of bcrypt
    bcrypt = Bcrypt(app)

    #load routes
    from user_routes import register_routes
    from contacts_routes import contact_routes
    register_routes(app, db, bcrypt)
    contact_routes(app, db)

    migrate = Migrate(app, db)

    return app