#!/usr/bin/python3
"""Defining the places module to request the places objs"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places(city_id):
    """get all places objects"""
    city = storage.all(City).get(f"City.{city_id}")
    if not city:
        abort(404)

    objs = []
    for obj in city.places:
        objs.append(obj.to_dict())

    return jsonify(objs)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """get a place object by id"""
    place = storage.all(Place).get(f"Place.{place_id}")
    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """delete a place object by id"""
    place = storage.all(Place).get(f"Place.{place_id}")
    if not place:
        abort(404)

    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """create a new place object"""
    city = storage.all(City).get(f"City.{city_id}")
    if not city:
        abort(404)

    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}, 400)
    if 'user_id' not in request.get_json():
        return jsonify({'error': 'Missing user_id'}, 400)

    user_id = request.get_json()['user_id']
    user = storage.all(User).get(f"User.{user_id}")
    if not user:
        abort(404)

    if 'name' not in request.get_json():
        return jsonify({'error': 'Missing name'}, 400)

    name = request.get_json()['name']
    place = Place(city_id=city_id, user_id=user_id, name=name)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """update place object"""
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400

    place = storage.all(Place).get(f"Place.{place_id}")
    if not place:
        abort(404)

    ignor = ["id", "created_at", "updated_at", "user_id", "city_id"]
    for k, v in request.get_json().items():
        if k in ignor:
            continue
        setattr(user, k, v)

    place.save()
    return jsonify(place.to_dict())
