from flask import Blueprint, jsonify, request
from .models import Interest, User
from . import db
interest = Blueprint('interest', __name__)

@interest.route('/interests', methods=['GET'])
def get_interests():
    """
    Get all interests, optionally filter by category.

    Query Parameters:
        category (optional): Filter interests by this category name.

    Response:
        200 OK
        [
            {"id": 1, "name": "Traveling", "category": "Hobbies & Activities"},
            {"id": 2, "name": "Gaming", "category": "Entertainment & Media"}
        ]
    """
    category = request.args.get('category', None)
    print(f"Filtering interests by category: {category}")
    if category:
        interests = Interest.query.filter_by(category=category).all()
    else:
        interests = Interest.query.all()

    interests_list = [
        {"id": i.id, "name": i.name, "category": i.category} for i in interests
    ]

    return jsonify(interests_list), 200



@interest.route('/interests/categories', methods=['GET'])
def get_interests_groupped_Category():

    category_filter = request.args.get('category', None)

    if category_filter:
        interests = Interest.query.filter_by(category=category_filter).all()
    else:
        interests = Interest.query.all()

    grouped = {}
    for i in interests:
        if i.category not in grouped:
            grouped[i.category] = []
        grouped[i.category].append({"id": i.id, "name": i.name})

    return jsonify(grouped), 200


# 1. **GET /api/interests** - Get all available interests (with optional category filter)
# 2. **GET /api/interests/categories** - Get all interests grouped by category
# 3. **POST /api/users/:id/interests** - Update user interests (replace existing)
# 4. **GET /api/users/:id/interests** - Get user's selected interests