from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from models import Contacts, Group, ContactHistory, db
import random
from datetime import datetime

contact_bp = Blueprint('contacts', __name__)

@contact_bp.route('/random_contact', methods=['GET', 'POST'])
@login_required
def random_contact():
    if request.method == 'GET':
        # Fetch the user's groups
        groups = Group.query.filter_by(user_id=current_user.uid).all()
        return render_template('random_contact.html', groups=groups)  # Pass groups to the template

    if request.method == 'POST':
        group_id = request.form.get('group_id')
        allow_repeat = request.form.get('allow_repeat') == 'on'

        if not group_id:
            return jsonify({'message': 'Group ID is required'}), 400

        group = Group.query.filter_by(id=group_id, user_id=current_user.uid).first()
        if not group:
            return jsonify({'message': 'Group not found'}), 404

        contacts = group.contacts
        if not contacts:
            return jsonify({'message': 'No contacts found in this group'}), 404

        if len(contacts) == 1:
            selected_contact = contacts[0]
        else:
            if allow_repeat:
                selected_contact = random.choice(contacts)
            else:
                last_contacted = ContactHistory.query.filter_by(user_id=current_user.uid, group_id=group_id).order_by(ContactHistory.last_contacted.desc()).first()
                if last_contacted:
                    contacts = [contact for contact in contacts if contact.id != last_contacted.contact_id]
                selected_contact = random.choice(contacts)

        # Update contact history
        contact_history = ContactHistory(
            user_id=current_user.uid,
            contact_id=selected_contact.id,
            group_id=group_id,
            
        )
        db.session.add(contact_history)
        db.session.commit()

        groups = Group.query.filter_by(user_id=current_user.uid).all()
        last_contacted_time = contact_history.last_contacted.strftime('%Y-%m-%d %H:%M:%S')
        return render_template('random_contact.html', groups=groups, selected_contact=selected_contact, last_contacted=last_contacted_time)