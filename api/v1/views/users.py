#!/usr/bin/python3
"""Defining the users module to request the users objs"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
def get_users():
    """get all users objects"""
    objs = []

    for obj in storage.all(User).values():
        objs.append(obj.to_dict())

    return jsonify(objs)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """get a user object by id"""
    user = storage.all(User).get(f"User.{user_id}")
    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """delete a user object by id"""
    user = storage.all(User).get(f"User.{user_id}")
    if not user:
        abort(404)

    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'])
def create_user():
    """create a new user object"""
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}, 400)
    if 'email' not in request.get_json():
        return jsonify({'error': 'Missing email'}, 400)
    if 'password' not in request.get_json():
        return jsonify({'error': 'Missing password'}, 400)

    user = User(email=request.get_json()['email'],
                password=request.get_json()['password'])
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """update user object"""
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400

    user = storage.all(User).get(f"User.{user_id}")
    if not user:
        abort(404)

    ignor = ["id", "created_at", "updated_at", "email"]
    for k, v in request.get_json().items():
        if k in ignor:
            continue
        setattr(user, k, v)

    user.save()
    return jsonify(user.to_dict())
