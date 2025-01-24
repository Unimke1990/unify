from datetime import datetime
from flask_login import login_required, current_user
from flask import Blueprint, request, render_template, url_for, redirect, flash
from models import Reminder, db


reminder_bp = Blueprint('reminders', __name__)

@reminder_bp.route('/reminders', methods=['GET'])
@login_required
def view_reminders():
    reminders = Reminder.query.filter_by(user_id=current_user.uid).all()
    return render_template('view_reminders.html', reminders=reminders)


@reminder_bp.route('/reminders/create', methods=['GET', 'POST'])
@login_required
def create_reminder():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        due_date = request.form.get('due_date')
        recurrence_type = request.form.get('recurrence_type')
        recurrence_frequency = request.form.get('recurrence_frequency')
        recurrence_interval = request.form.get('recurrence_interval')

        reminder = Reminder(
            title=title,
            description=description,
            due_date=datetime.strptime(due_date, '%Y-%m-%d %H:%M:%S'),
            user_id=current_user.uid,
            recurrence_type=recurrence_type,
            recurrence_frequency=int(recurrence_frequency) if recurrence_frequency else None,
            recurrence_interval=int(recurrence_interval) if recurrence_interval else None
        )
        db.session.add(reminder)
        db.session.commit()
        flash('Reminder created successfully.')
        return redirect(url_for('reminders.view_reminders'))

    return render_template('create_reminder.html')


@reminder_bp.route('/reminders/edit_reminder/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_reminder(id):
    reminder = Reminder.query.get_or_404(id)
    if reminder.user_id != current_user.uid:
        flash('You do not have permission to edit this reminder')
        return redirect(url_for('reminders.view_reminders'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        due_date = request.form.get('due_date')
        recurrence_type = request.form.get('recurrence_type')
        recurrence_frequency = request.form.get('recurrence_frequency')
        recurrence_interval = request.form.get('recurrence_interval')
             
        # Update existing reminder object    
        reminder.title = title
        reminder.description = description
        reminder.due_date = datetime.strptime(due_date, '%Y-%m-%d %H:%M:%S')
        reminder.recurrence_type = recurrence_type
        reminder.recurrence_frequency = int(recurrence_frequency) if recurrence_frequency else None
        reminder.recurrence_interval = int(recurrence_interval) if recurrence_interval else None
        
        db.session.commit()
        flash('Reminder edited and updated successfully.')
        return redirect(url_for('reminders.view_reminders'))
    
    return render_template('edit_reminder.html', reminder=reminder)


@reminder_bp.route('/reminders/delete/<int:id>', methods=['POST'])
@login_required
def delete_reminder(id):
    reminder = Reminder.query.get_or_404(id)
    if reminder.user_id != current_user.uid:
        flash('You do not have permission to delete this reminder.')
        return redirect(url_for('reminders.view_reminders'))

    db.session.delete(reminder)
    db.session.commit()
    flash('Reminder deleted successfully.')
    return redirect(url_for('reminders.view_reminders'))
   