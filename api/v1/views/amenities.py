#!/usr/bin/python3
"""Defining the amenities module"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def get_amenities():
    """get all Amenities objects"""
    objs = []

    for obj in storage.all(Amenity).values():
        objs.append(obj.to_dict())

    return jsonify(objs)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """get an amenity object by id"""
    ame = storage.all(Amenity).get(f"Amenity.{amenity_id}")
    if not ame:
        abort(404)

    return jsonify(ame.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """delete an amenity object by id"""
    ame = storage.all(Amenity).get(f"Amenity.{amenity_id}")
    if not ame:
        abort(404)

    ame.delete()
    storage.save()
    return jsonify({})


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """create a new amenity object"""
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}, 400)
    if 'name' not in request.get_json():
        return jsonify({'error': 'Missing name'}, 400)

    ame = Amenity(name=request.get_json()['name'])
    ame.save()
    return jsonify(ame.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """update amenity object"""
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400

    ame = storage.all(Amenity).get(f"Amenity.{amenity_id}")
    if not ame:
        abort(404)

    for k, v in request.get_json().items():
        if k == "id" or k == "created_at" or k == "updated_at":
            continue
        setattr(ame, k, v)

    ame.save()
    return jsonify(ame.to_dict()), 200
