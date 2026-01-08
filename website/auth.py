from flask import Blueprint, render_template, request, flash, redirect
import string
from .models import User, Note
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, logout_user, login_required


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter(
            (User.email == email)).first()

    if not user:
        flash('Email does not exist.', category='error')
        return render_template('login.html')
    if not check_password_hash(user.password, password):
        flash('Incorrect password, try again.', category='error')
        return render_template('login.html')
    
    login_user(user, remember=True)
    flash(f"Welcome back, {user.first_name}!", category='success')
    return render_template('dashboard.html')

@auth.route('/logout')
def logout():
    return "<p>logout</p>" 

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    data = request.form
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        age = request.form.get('age')
        sex = request.form.get('sex')
        sexual_preference = request.form.get('sexualPreference')

        if (len(username) < 4):
            flash("username too short", category='error')
        if any(char in string.punctuation for char in password) == False:
            flash("password must contain at least one special character", category='error')
        if (len(password) < 8 ):
            flash("password must contain at least 8 character", category="error")

        user = User(email=email, username=username, password=generate_password_hash(password, method='pbkdf2:sha256'), first_name=first_name, last_name=last_name, age=age, sex=sex, sexualPreference=sexual_preference)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', category='success')
        return render_template('dashboard.html')
    return render_template('sign-up.html')



