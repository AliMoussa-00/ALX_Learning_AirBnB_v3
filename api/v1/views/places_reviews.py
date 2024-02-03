#!/usr/bin/python3
"""Defining the places reviews module to request the reviews objs"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_place_reviews(place_id):
    """get a place's reviews object by id"""
    place = storage.all(Place).get(f"Place.{place_id}")
    if not place:
        abort(404)
    reviews = []
    for rev in place.reviews:
        reviews.append(rev.to_dict())

    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_reviews(review_id):
    """get a review object by id"""
    rev = storage.all(Review).get(f"Review.{review_id}")
    if not rev:
        abort(404)

    return jsonify(rev.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """delete a review object by id"""
    rev = storage.all(Review).get(f"Review.{review_id}")
    if not rev:
        abort(404)

    rev.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """create a new review object"""
    place = storage.all(Place).get(f"Place.{place_id}")
    if not place:
        abort(404)

    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    if 'user_id' not in request.get_json():
        return jsonify({'error': 'Missing user_id'}), 400

    user_id = request.get_json()['user_id']
    user = storage.all(User).get(f"User.{user_id}")
    if not user:
        abort(404)

    if 'text' not in request.get_json():
        return jsonify({'error': 'Missing text'}), 400

    text = request.get_json()['text']
    review = Review(place_id=place_id, user_id=user_id, text=text)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """update review object"""
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400

    rev = storage.all(Review).get(f"Review.{review_id}")
    if not rev:
        abort(404)

    ignor = ["id", "created_at", "updated_at", "user_id", "place_id"]
    for k, v in request.get_json().items():
        if k in ignor:
            continue
        setattr(rev, k, v)

    rev.save()
    return jsonify(rev.to_dict())
