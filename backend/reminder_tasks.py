from datetime import datetime
from flask import current_app
from models import Reminder
from flask_mail import Message
from extensions import mail, db

# Global variable to store the Flask application instance
app = None

# Function to set the global app variable
def set_app(application):
    global app
    app = application

# Send email reminder
def send_reminder_email(reminder):
    msg = Message(subject=f"Reminder: {reminder.title}",
                  body=f"Reminder: {reminder.title}\n\n{reminder.description}\n\nDue: {reminder.due_date}",
                  recipients=[reminder.user.email])
    mail.send(msg)

# Check for reminders
def check_reminders():
    global app
    with app.app_context():
        now = datetime.utcnow()
        reminders = Reminder.query.filter(Reminder.due_date <= now).all()
        for reminder in reminders:
            send_reminder_email(reminder)
            db.session.delete(reminder)
        db.session.commit()