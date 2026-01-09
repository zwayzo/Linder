from flask import Blueprint, render_template, request, flash, redirect, jsonify, current_app
import string
from .models import Profile, User, Interest
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, logout_user, login_required, current_user as curr
import jwt
from datetime import datetime, timedelta
from functools import wraps

user = Blueprint('user', __name__)


@user.route('/<int:user_id>', methods=['GET'])
def get_user_profile(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    profile = Profile.query.filter_by(user_id=user.id).first()
    interests = [interest.name for interest in profile.interests]

    user_data = {
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
    }

    return jsonify(user_data), 200