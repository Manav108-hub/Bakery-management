from flask import Blueprint, request, jsonify
from src.models.models import User, db
from flask_jwt_extended import create_access_token
import datetime
import os

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Check for API key
    api_key = request.headers.get('X-API-Key')
    expected_api_key = os.getenv('API_KEY')
    
    if not api_key or api_key != expected_api_key:
        return jsonify({"error": "Invalid or missing API key"}), 401
    
    if not data or 'username' not in data or 'password' not in data or 'email' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists"}), 409
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already exists"}), 409
    
    # Allow setting admin status if provided
    is_admin = bool(data.get('is_admin', False))
    
    new_user = User(
        username=data['username'],
        email=data['email'],
        is_admin=is_admin  # Use the value from the request
    )
    new_user.set_password(data['password'])
    
    db.session.add(new_user)
    db.session.commit()
    
    # Generate auth token for the new user
    expires = datetime.timedelta(days=7)
    access_token = create_access_token(identity={
        'id': new_user.id,
        'username': new_user.username,
        'is_admin': new_user.is_admin
    }, expires_delta=expires)
    
    return jsonify({
        "message": "User created successfully",
        "auth_token": access_token,
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "is_admin": new_user.is_admin
        }
    }), 201

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Check for API key
    api_key = request.headers.get('X-API-Key')
    expected_api_key = os.getenv('API_KEY')
    
    if not api_key or api_key != expected_api_key:
        return jsonify({"error": "Invalid or missing API key"}), 401
    
    if not data or ('username' not in data and 'email' not in data) or 'password' not in data:
        return jsonify({"error": "Missing username/email or password"}), 400
    
    # Find user by username OR email
    if 'username' in data:
        user = User.query.filter_by(username=data['username']).first()
    else:
        user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({"error": "Invalid credentials"}), 401
    
    expires = datetime.timedelta(days=7)
    access_token = create_access_token(identity={
        'id': user.id,
        'username': user.username,
        'is_admin': user.is_admin
    }, expires_delta=expires)
    
    return jsonify({
        "auth_token": access_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }), 200