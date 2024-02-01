#!/usr/bin/python3
"""Defining the index module"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def get_status():
    """get the status code"""
    return jsonify({"status": "OK"})
