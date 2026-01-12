from flask import Blueprint, render_template, request, flash, redirect, jsonify, current_app
import string

from website import user
from .models import Profile, User, Interest
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, mail
from flask_login import login_user, logout_user, login_required, current_user as curr
import jwt
from datetime import datetime, timedelta
from functools import wraps
import secrets
from flask_mail import Message

auth = Blueprint('auth', __name__)


def generate_token(user_id, expires_in=3600):
    """Generate a JWT token for a user"""
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(seconds=expires_in)
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Get token from Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"error": "Token is missing"}), 401

        try:
            # ✅ Use current_app here
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except Exception as e:
            return jsonify({"error": "Invalid token", "details": str(e)}), 401

        return f(current_user, *args, **kwargs)
    return decorated



def send_mail(user, token):
    # token = secrets.token_urlsafe(32)
    # user.email_token_hash = generate_password_hash(token)
    # user.email_token_expiry = datetime.utcnow() + timedelta(hours=24)  # link valid 24h
    # db.session.commit()
    # print("user token hash:", user.email_token_hash)
    # print("user token expiry:", user.email_token_expiry)
    
    
    confirm_link = f"http://localhost:5000/auth/confirm-email?token={token}"

    msg = Message(
        subject="Confirm your email",
        recipients=[user.email]
    )
    msg.body = f"""
    Hi {user.first_name},

    Thanks for signing up! Click the link below to confirm your email:

{   confirm_link}

    This link expires in 24 hours.

    If you did not sign up, ignore this email.
"""
    mail.send(msg)
    return "✅ Your email has been sent!"
    



@auth.route('/confirm-email', methods=['GET'])
def confirm_email():
    token = request.args.get('token')
    print("Received token:", token)
    if not token:
        return "Invalid confirmation link", 400

    users = User.query.filter(User.reset_token_expiry > datetime.utcnow()).all()
    matched_user = None
    for u in users:
        if check_password_hash(u.reset_token_hash, token):
            matched_user = u
            break

    if not matched_user:
        return "Invalid or expired token", 400

    # Mark email as verified
    matched_user.is_email_verified = True
    matched_user.reset_token_hash = None
    matched_user.reset_token_expiry = None
    matched_user.emailVerified = True 
    db.session.commit()

    return "✅ Your email has been confirmed!"






@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter(
            (User.email == email)).first()

    if not user:
        return jsonify({"error": "User not found"}), 404
    if not check_password_hash(user.password, password):
        return jsonify({"error": "Wrong password"}), 401
    
    login_user(user, remember=True)
    token = generate_token(user.id)
    user.profile.online = True
    flash(f"Welcome back, {user.first_name}!", category='success')
    return jsonify({
        "message": "Login successful",
        "token": token,
        "user_id": user.id,
        "email": user.email
    }), 200 

@login_required
@auth.route('/logout')
def logout():
    user = request.user()
    user.profile.online = False

    logout_user()
    return jsonify({
        "message": "Successfully logged out"
    }), 200 




@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    data = request.get_json()
    if request.method == 'POST':
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        age = data.get('age')
        sex = data.get('sex')
        sexual_preference = data.get('sexualPreference')
        title = data.get('title')
        company = data.get('company')
        bio = data.get('bio')
        interests_list = data.get('interests', [])  # List of interest names
        education = data.get('education')
        experience_level = data.get('experienceLevel')
        industry = data.get('industry')
        image1 = data.get('image1')
        image2 = data.get('image2')
        image3 = data.get('image3')
        image4 = data.get('image4')

        if len(interests_list) < 6:
            return jsonify({"error": "Select at least 6 interests"}), 400

        mail_token = secrets.token_urlsafe(32)
        user = User(email=email, username=username, 
                    password=generate_password_hash(password, method='pbkdf2:sha256'), 
                    first_name=first_name, last_name=last_name, age=age, sex=sex, 
                    sexualPreference=sexual_preference,
                    reset_token_hash = generate_password_hash(mail_token),
                    reset_token_expiry = datetime.utcnow() + timedelta(hours=24))
        db.session.add(user)
        db.session.commit()
        
        # 2️⃣ Create the profile linked to the user
        profile = Profile(
            user_id=user.id,
            title=title,
            company=company,
            bio=bio,
            education=education,
            experienceLevel=experience_level,
            industry=industry,
            image1=image1,
            image2=image2,
            image3=image3,
            image4=image4
        )
        for interest_name in interests_list:
            interest = Interest.query.filter_by(name=interest_name).first()
            if interest:
                profile.interests.append(interest)

    db.session.add(profile)
    db.session.commit()
    user.profile.online = True
    # login_user(user, remember=True)
    token = generate_token(user.id)
    
    send_mail(user, mail_token)
    
    return jsonify({
        "message": "Account created successfully!",
        "token": token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        },
        "profile": {
            "id": profile.id,
            "title": profile.title,
            "company": profile.company,
            "interests": [i.name for i in profile.interests]
        }
    }), 201



@auth.route('/me', methods=['GET'])
# @login_required
@token_required
def get_current_user(current_user):
    user = current_user
    if not user:
        return jsonify({"error": "User not found"}), 404

    profile = user.profile
    interests = [interest.name for interest in profile.interests]

    return jsonify({
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "age": user.age
        },
        "profile": {
            "id": profile.id,
            "title": profile.title,
            "company": profile.company,
            "bio": profile.bio,
            "education": profile.education,
            "experienceLevel": profile.experienceLevel,
            "industry": profile.industry,
            "image1": profile.image1,
            "image2": profile.image2,
            "image3": profile.image3,
            "image4": profile.image4,
            "interests": interests
        }
    }), 200
    



@auth.route('/forgot-password', methods=['POST'])
def request_reset_password():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"error": "Email is required"}), 400

    user = User.query.filter_by(email=email).first()

    if user:
        # Generate token
        token = secrets.token_urlsafe(32)
        user.reset_token_hash = generate_password_hash(token)
        user.reset_token_expiry = datetime.utcnow() + timedelta(minutes=15)
        db.session.commit()

        # Create clickable reset link pointing to backend
        reset_link = f"http://localhost:5000/auth/reset-password/confirm?token={token}"

        # Send email
        msg = Message(
            subject="Reset Your Password",
            recipients=[user.email]
        )
        msg.body = f"""
Hello,

You requested a password reset. Click the link below to reset your password:

{reset_link}

This link expires in 15 minutes.

If you did not request this, ignore this email.
"""
        
        
        try:
            mail.send(msg)
            print("✅ Reset email sent successfully!")
        except Exception as e:
            print("❌ Error sending email:", e)

    # Always return generic message
    return jsonify({"token": token,
        "message": "If this email exists, a reset link has been sent."})




@auth.route('/reset-password/', methods=['POST'])
def confirm_reset_password():
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('new_password')

    if not token or not new_password:
        return jsonify({"error": "Token and new password are required"}), 400

    # Find user with valid token
    users = User.query.filter(User.reset_token_expiry > datetime.utcnow()).all()
    matched_user = None
    for u in users:
        if check_password_hash(u.reset_token_hash, token):
            matched_user = u
            break

    if not matched_user:
        return jsonify({"error": "Invalid or expired token"}), 400

    # Update password
    matched_user.password = generate_password_hash(new_password)

    # Invalidate token
    matched_user.reset_token_hash = None
    matched_user.reset_token_expiry = None

    db.session.commit()

    return jsonify({"message": "Password has been reset successfully"}), 200



