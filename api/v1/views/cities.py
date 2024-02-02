#!/usr/bin/python3
"""Defining the cities module to request the cities objs"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.city import City
from models import storage
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_state_cities(state_id):
    """get a state object by id"""
    state = storage.all(State).get(f"State.{state_id}")
    if not state:
        abort(404)
    state_cities = []
    for city in state.cities:
        state_cities.append(city.to_dict())

    return jsonify(state_cities)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """get a city object by id"""
    city = storage.all(City).get(f"City.{city_id}")
    if not city:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """delete a city object by id"""
    city = storage.all(City).get(f"City.{city_id}")
    if not city:
        abort(404)

    city.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """create a new city object"""
    state = storage.all(State).get(f"State.{state_id}")
    if not state:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}, 400)
    if 'name' not in request.get_json():
        return jsonify({'error': 'Missing name'}, 400)

    city = City(name=request.get_json()['name'], state_id=state_id)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """update city object"""
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400

    city = storage.all(City).get(f"City.{city_id}")
    if not city:
        abort(404)

    for k, v in request.get_json().items():
        if k == "id" or k == "created_at" or k == "updated_at":
            continue
        setattr(city, k, v)

    city.save()
    return jsonify(city.to_dict())
