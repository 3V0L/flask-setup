from flask import Blueprint, jsonify


api = Blueprint('api', __name__)

@api.route('/', methods=['GET'])
def home():
    """Returns home page for API"""
    return jsonify({'msg': 'Welcome to the API!'}), 200
