from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import Contacts, Group, ContactHistory, db
import random
from datetime import datetime

contact_bp = Blueprint('contacts', __name__)

@contact_bp.route('/random_contact', methods=['POST'])
@login_required
def random_contact():
    data = request.get_json()
    group_id = data.get('group_id')
    allow_repeat = data.get('allow_repeat', False)

    if not group_id:
        return jsonify({'message': 'Group ID is required'}), 400

    group = Group.query.filter_by(id=group_id, user_id=current_user.id).first()
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
            last_contacted = ContactHistory.query.filter_by(user_id=current_user.id, group_id=group_id).order_by(ContactHistory.last_contacted.desc()).first()
            if last_contacted:
                contacts = [contact for contact in contacts if contact.id != last_contacted.contact_id]
            selected_contact = random.choice(contacts)

    # Update contact history
    contact_history = ContactHistory(
        user_id=current_user.id,
        contact_id=selected_contact.id,
        group_id=group_id,
        last_contacted=datetime.utcnow()
    )
    db.session.add(contact_history)
    db.session.commit()

    return jsonify({
        'id': selected_contact.id,
        'name': selected_contact.name,
        'phone': selected_contact.phone,
        'email': selected_contact.email
    }), 200