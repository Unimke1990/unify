from flask_login import login_user, logout_user, login_required, current_user
from flask import request, render_template, url_for, redirect, flash
from models import Users, Contacts, Reminder
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt
import re

def contact_routes(app, db):
    """
    Define routes for contact management.

    Parameters:
    app (Flask): The Flask application instance.
    db (SQLAlchemy): The SQLAlchemy database instance.
    """
    @app.route('/add_contact', methods=['GET', 'POST'])
    @login_required
    def add_contact():
        """
        Handle the addition of new contacts via GET and POST requests.
        """
        if request.method == 'GET':
            return render_template('add_contact.html')
        elif request.method == 'POST':
            name = request.form.get('name').strip().lower()
            email = request.form.get('email').strip().lower()
            phone = request.form.get('phone').strip()

            # Validate input
            if not name or not email or not phone:
                flash('All fields are required.')
                return redirect(url_for('add_contact'))

            # validate phone numbers
            number_pattern = r'^\+?[1-9]\d{1,14}$'
            if not re.match(number_pattern, phone):
                flash('Invalid phone number')
                return redirect(url_for('add_contact')) 

            # Validate name
            name_regex = r'^[a-zA-Z]+(?: [a-zA-Z]+)*$'
            if not re.match(name_regex, name):
                flash('Invalid name format')
                return redirect(url_for('add_contact'))
            
            # Validate email format
            email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
            if not re.match(email_regex, email):
                flash('Invalid email format')
                return redirect(url_for('add_contact'))
            
            # Checks if email already exists
            existing_contact = Contacts.query.filter_by(email=email).first()
            if existing_contact:
                flash('Email is already in use.')
                return redirect(url_for('add_contact'))
            
            # Create new contacts
            new_contact = Contacts(name=name, email=email, phone=phone, user_id=current_user.uid)

            try:
                db.session.add(new_contact)
                db.session.commit()
                flash('Contact added successfully')
                return redirect(url_for('index'))
            except IntegrityError:
                db.session.rollback()
                flash('An error occurred while adding the contact. Please try again.')
            return redirect(url_for('add_contact'))


    @app.route('/contacts')
    @login_required
    def contacts():
        """
        function that returns all contacts of current user
        """
        contacts = current_user.contacts.all()
        return render_template('contacts.html', contacts=contacts)


    @app.route('/edit_contact/<int:id>', methods=['GET', 'POST'])
    @login_required
    def edit_contact(id):
        """
        function that edits a contact
        """
        contact = Contacts.query.get(id)
        if not contact:
            flash('Contact not found')
            return redirect(url_for('contacts'))
        if request.method == 'GET':
            return render_template('edit_contact.html', contact=contact)
        elif request.method == 'POST':
            name = request.form.get('name').strip().lower()
            email = request.form.get('email').strip().lower()
            phone = request.form.get('phone').strip()

            # Validate input
            # if not name or not email or not phone:
            #     flash('All fields are required.')
            #     return redirect(url_for('edit_contact', id=id))

            # validate phone numbers
            number_pattern = r'^\+?[1-9]\d{1,14}$'
            if not re.match(number_pattern, phone):
                flash('Invalid phone number')
                return redirect(url_for('edit_contact', id=id)) 

            # Validate name
            name_regex = r'^[a-zA-Z]+(?: [a-zA-Z]+)*$'
            if not re.match(name_regex, name):
                flash('Invalid name format')
                return redirect(url_for('edit_contact', id=id))
            
            # Validate email format
            email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
            if not re.match(email_regex, email):
                flash('Invalid email format')
                return redirect(url_for('edit_contact', id=id))
            
            # Checks if email already exists
            existing_contact = Contacts.query.filter_by(email=email).first()
            if existing_contact and existing_contact.email != contact.email:
                flash('Email is already in use.')
                return redirect(url_for('edit_contact', id=id))
            
            contact.name = name
            contact.email = email
            contact.phone = phone

            try:
                db.session.commit()
                flash('Contact updated successfully')
                return redirect(url_for('contacts'))
            except IntegrityError:
                db.session.rollback()
                flash('An error occurred while updating the contact. Please try again.')
            return redirect(url_for('edit_contact', id=id))

    
    @app.route('/delete_contact/<int:id>')
    @login_required
    def delete_contact(id):
        """
        function that deletes a contact
        """
        contact = Contacts.query.get(id)
        if not contact:
            flash('Contact not found')
            return redirect(url_for('contacts'))
        db.session.delete(contact)
        db.session.commit()
        flash('Contact deleted successfully')
        return redirect(url_for('contacts'))

            
        