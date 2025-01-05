from flask_login import login_user, logout_user, login_required, current_user
from flask import request, render_template, url_for, redirect, flash
from models import Users, Contacts, Reminder
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt
import re

def reminders_routes(app, db):
    @app.routes('/add_reminders', methods=['GET', 'POST'])
    @login_required
    def add_reminders():
        pass