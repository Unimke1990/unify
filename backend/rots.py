from flask_login import login_user, logout_user, login_required, current_user
from flask import request, render_template, url_for, redirect, flash
from models import Users, Contacts, Reminder
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt


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

            #validate password length
            if len(password) < 6:
                flash('Password must be at least 6 characters long')
                return redirect(url_for('signup'))
            
            #create a new user instance
            user = Users(name=name, username=username, password=password, email=email)

            try:
                db.session.add(user)
                db.session.commit()
                flash('User created successfully, please login.')
                return redirect(url_for('login'))
            except IntegrityError:
                db.session.rollback()
                flash('Username or email already exists')
                return redirect(url_for('signup'))

    

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            user = Users.query.filter_by(username=username).first()
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