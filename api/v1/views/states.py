#!/usr/bin/python3
"""Defining the state module to retrieve the state objs"""

from api.v1.views import app_views
from flask import jsonify
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'])
def get_states():
    """get all States objects"""
    objs = []

    for obj in storage.all(State).values():
        objs.append(obj.to_dict())

    return jsonify(objs)

'''
@app_views.route('/states/')
def get_state_by_id():
    """get a state object by id"""
    return jsonify()
'''
