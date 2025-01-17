import os
from flask import Flask, url_for, request, flash, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_mail import Mail
from datetime import timedelta
from extensions import mail, login_manager, bcrypt, db


def create_app():
    """
    Initializes and configures the Flask application
    """
    app = Flask(__name__, template_folder='templates')

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql+psycopg2://postgres:1990@localhost:5432/unifydb')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '1990_stylen9JA')
    app.config['SECURITY_PASSWORD_SALT'] = os.getenv('SECURITY_PASSWORD_SALT', 'my_precious_two')
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

    # Flask-Mail configuration for Gmail
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'agimagba1990@gmail.com')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'mhea jfpl hzvd vtwn')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'Unify App <agimagba1990@gmail.com>')


    public_endpoints = ['index', 'auth.login', 'auth.signup', 'auth.verify_email']
    @app.before_request
    def refresh_session():
        session.modified = True
        if not current_user.is_authenticated and request.endpoint not in public_endpoints:
            flash('Your session has expired. Please log in again.')
            return redirect(url_for('auth.login'))

    # Initialize extensions
    mail.init_app(app)
    db.init_app(app)
    Migrate(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(uid):
        user = Users.query.get(uid)
        return user if user else None

    #login required manager for update_profile, and delete_profile
    @login_manager.unauthorized_handler
    def unauthorized():
        # Determine which route triggered the unauthorized request
        if request.path == url_for('update_profile'):
            flash('You must be logged in before you can update your profile')
            return redirect(url_for('auth.login'))

        elif request.path == url_for('delete_account'):
            flash('You must be logged in before you can delete your account')
            return redirect(url_for('auth.login'))

        elif request.path == url_for('add_contact'):
            flash('You must be logged in before you can add a contact')
            return redirect(url_for('auth.login'))

        elif request.path == url_for('contacts'):
            flash('You must be logged in before you can view your contacts')
            return redirect(url_for('auth.login'))
        
        elif request.path == url_for('edit_contact'):
            flash('You must be logged in before you can edit your contacts')
            return redirect(url_for('auth.login'))
        
        elif request.path == url_for('delete_contact'):
            flash('You must be logged in before you can delete your contacts')
            return redirect(url_for('auth.login'))

        else:
            flash('You must be logged in to access this page')
            return redirect(url_for('auth.login'))
        
     #load models
    from models import Users, Contacts, Group, Reminder

    # Register routes
    from contacts_routes import contact_routes
    from user_routes import register_routes
    from auth_routes import auth_bp
    from reminder_routes import reminder_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    register_routes(app, db, bcrypt)
    contact_routes(app, db)
    app.register_blueprint(reminder_bp, url_prefix='/reminders')
    app.register_blueprint(contact_bp, url_prefix='/contacts')
    
    return app