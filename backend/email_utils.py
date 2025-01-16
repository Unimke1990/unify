from flask_mail import Message
from flask import url_for
from extensions import mail
from utils import generate_verification_token

def send_verification_email(user_email):
    token = generate_verification_token(user_email)
    verification_url = url_for('auth.verify_email', token=token, _external=True)
    html = f'<p>Please click the link to verify your email: <a href="{verification_url}">{verification_url}</a></p>'
    subject = "Please verify your email"
    msg = Message(subject, recipients=[user_email], html=html)
    mail.send(msg)