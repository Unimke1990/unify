from flask_login import login_user, logout_user, login_required, current_user
from flask import request, render_template, url_for, redirect, flash
from models import Users, Contacts, Reminder
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt
import re


def register_routes(app, db, bcrypt):

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'GET':
            return render_template ('signup.html')
        elif request.method == 'POST':
            name = request.form.get('name').strip()
            username = request.form.get('username').strip()
            password = request.form.get('password').strip()
            email = request.form.get('email').strip()

            #validate input
            if not name or not username or not password or not email:
                flash('All fields are required.')
                return redirect(url_for('signup'))
            
            #validate name
            name_regex = r'^[a-zA-Z]{2,}$'
            if not re.match(name_regex, name):
                flash('Invalid name format')
                return redirect(url_for('signup'))
            
            #validate email format
            email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
            if not re.match(email_regex, email):
                flash('Invalid email format')
                return redirect(url_for('signup'))
            
            #validate username format
            username_regex = r'^[a-zA-Z0-9](?:[a-zA-Z0-9_]{2,14}[a-zA-Z0-9])?$'
            if not re.match(username_regex, username):
                flash('Invalid username format')
                return redirect(url_for('signup'))
            
            #validate password length
            if len(password) < 6:
                flash('Password must be at least 6 characters long')
                return redirect(url_for('signup'))
            
            #create a new user instance
            try:
                user = Users(name=name, username=username, password=password, email=email)
            except AttributeError as e:
                flash(f'Error: {str(e)}')
                return redirect(url_for('signup'))

            try:
                db.session.add(user)
                db.session.commit()
                flash('User created successfully, please login.')
                return redirect(url_for('login'))
            except IntegrityError:
                db.session.rollback()
                flash('Username or email already exists')
                return redirect(url_for('signup'))
            except Exception as e:
                flash(f'Error: {str(e)}')
                return redirect(url_for('signup'))

    

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            username = request.form.get('username').strip()
            password = request.form.get('password').strip()

            #checking for empty fields
            if not username or not password:
                flash('Username and password required')
                return redirect(url_for('login'))
            #username format checks
            username_regex = r'^[a-zA-Z0-9](?:[a-zA-Z0-9_]{2,14}[a-zA-Z0-9])?$'
            if not re.match(username_regex, username):
                flash('Invalid username format')
                return redirect(url_for('login'))
            
            #check username in database
            try:
                user = Users.query.filter_by(username=username).first()
            except Exception as e:
                flash(f'Database error: {str(e)}')
                return redirect(url_for('login'))
            
            if user and user.check_password(password):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash('Invalid username or password')
                return redirect(url_for('login'))
            
    

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('index'))