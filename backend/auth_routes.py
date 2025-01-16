from flask import Blueprint, request, render_template, url_for, redirect, flash, jsonify, session
from flask_login import login_user, logout_user
from models import Users, db
from utils import confirm_verification_token
from email_utils import send_verification_email
from sqlalchemy.exc import IntegrityError
import re

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        name = request.form.get('name').strip().lower()
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()
        email = request.form.get('email').strip()

        # Validate input
        if not name or not username or not password or not email:
            flash('All fields are required.')
            return redirect(url_for('auth.signup'))

        # Validate name
        name_regex = r'^[a-zA-Z]+(?: [a-zA-Z]+)*$'
        if not re.match(name_regex, name):
            flash('Invalid name format')
            return redirect(url_for('auth.signup'))

        # Validate email format
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if not re.match(email_regex, email):
            flash('Invalid email format')
            return redirect(url_for('auth.signup'))

        # Validate username format
        username_regex = r'^[a-zA-Z0-9](?:[a-zA-Z0-9_]{2,14}[a-zA-Z0-9])?$'
        if not re.match(username_regex, username):
            flash('Invalid username format')
            return redirect(url_for('auth.signup'))

        # Validate password length
        if len(password) < 6:
            flash('Password must be at least 6 characters long')
            return redirect(url_for('auth.signup'))

        # Create a new user instance
        try:
            user = Users(name=name, username=username, password=password, email=email)
        except AttributeError as e:
            flash(f'Error: {str(e)}')
            return redirect(url_for('auth.signup'))

        try:
            db.session.add(user)
            db.session.commit()
            send_verification_email(user.email)
            flash('User created successfully. Please check your email to verify your account.')
            return redirect(url_for('auth.login'))
        except IntegrityError:
            db.session.rollback()
            flash('Username or email already exists')
            return redirect(url_for('auth.signup'))
        except Exception as e:
            flash(f'Error: {str(e)}')
            return redirect(url_for('auth.signup'))
        

@auth_bp.route('/verify/<token>', methods=['GET'])
def verify_email(token):
    try:
        email = confirm_verification_token(token)
    except:
        flash('The verification link is invalid or has expired.', 'danger')
        return redirect(url_for('auth.login'))

    user = Users.query.filter_by(email=email).first_or_404()
    if user.email_verified:
        flash('Account already verified. Please login.', 'success')
    else:
        user.email_verified = True
        db.session.commit()
        flash('You have verified your account. Thanks!', 'success')
    return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()

        # Checking for empty fields
        if not username or not password:
            flash('Username and password required')
            return redirect(url_for('auth.login'))

        # Username format checks
        username_regex = r'^[a-zA-Z0-9](?:[a-zA-Z0-9_]{2,14}[a-zA-Z0-9])?$'
        if not re.match(username_regex, username):
            flash('Invalid username format')
            return redirect(url_for('auth.login'))

        # Check username in database
        try:
            user = Users.query.filter_by(username=username).first()
        except Exception as e:
            flash(f'Database error: {str(e)}')
            return redirect(url_for('auth.login'))

        if user and user.check_password(password):
            login_user(user)
            session.permanent = True
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
