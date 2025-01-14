from flask_login import login_user, logout_user, login_required, current_user
from flask import request, render_template, url_for, redirect, flash
from models import Users, Group, Contacts, Reminder
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt
import re
from flask import session

def register_routes(app, db, bcrypt):

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/update_profile', methods=['GET', 'POST'])
    @login_required
    def update_profile():
        if request.method == 'GET':
            return render_template('update_profile.html')
        elif request.method == 'POST':
            name = request.form.get('name').strip()
            username = request.form.get('username').strip()
            password = request.form.get('password').strip()
            email = request.form.get('email').strip()

            # Validate inputs
            # Validate name
            name_regex = r'^[a-zA-Z]+(?: [a-zA-Z]+)*$'
            if not re.match(name_regex, name):
                flash('Invalid name format')
                return redirect(url_for('update_profile'))

            # Validate email format
            email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
            if not re.match(email_regex, email):
                flash('Invalid email format')
                return redirect(url_for('update_profile'))

            # Validate username format
            username_regex = r'^[a-zA-Z0-9](?:[a-zA-Z0-9_]{2,14}[a-zA-Z0-9])?$'
            if not re.match(username_regex, username):
                flash('Invalid username format')
                return redirect(url_for('update_profile'))

            # Validate password format
            if password and len(password) < 6:
                flash('Password must be at least 6 characters long')
                return redirect(url_for('update_profile'))

            # Update user's details in database
            try:
                current_user.name = name
                current_user.username = username
                current_user.email = email
                if password:
                    current_user.password = bcrypt.generate_password_hash(password).decode('utf-8')
                db.session.commit()
                flash('Profile updated successfully.')
                logout_user()
                return redirect(url_for('auth.login'))
            except Exception as e:
                flash(f'Error: {str(e)}')
                return redirect(url_for('update_profile'))

    @app.route('/delete_account', methods=['POST'])
    @login_required
    def delete_account():
        try:
            db.session.delete(current_user)
            db.session.commit()
            flash('Profile deleted successfully.')
            logout_user()
            return redirect(url_for('auth.signup'))
        except Exception as e:
            flash(f'Error: {str(e)}')
            return redirect(url_for('update_profile'))

    @app.route('/logout')
    def logout():
        """
        Logs out the current user and redirects to the index page.
        """
        logout_user()
        session.clear()
        return redirect(url_for('index'))