from flask import Blueprint, request, jsonify
from .user_service import UserService
from marshmallow import ValidationError

user_bp = Blueprint('users', __name__)
user_service = UserService()

@user_bp.route('/users', methods=['GET'])
def get_users():
    try:
        users = user_service.get_all_users()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = user_service.get_user_by_id(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({'error': 'User not found'}), 404

@user_bp.route('/users', methods=['POST'])
def create_user():
    try:
        user_data = request.get_json()
        new_user = user_service.create_user(user_data)
        return jsonify(new_user), 201
    except ValidationError as err:
        return jsonify(err.messages), 400
    except ValueError as err:
        return jsonify({'error': str(err)}), 409

@user_bp.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        user_data = request.get_json()
        updated_user = user_service.update_user(user_id, user_data)
        if updated_user:
            return jsonify(updated_user), 200
        return jsonify({'error': 'User not found'}), 404
    except ValidationError as err:
        return jsonify(err.messages), 400
    except ValueError as err:
        return jsonify({'error': str(err)}), 400

@user_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_service.delete_user(user_id):
        return '', 204
    return jsonify({'error': 'User not found'}), 404