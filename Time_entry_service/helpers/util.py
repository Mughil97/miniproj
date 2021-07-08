from flask import make_response, jsonify

def send_response(result, status):
    response = make_response(jsonify(result), status)
    response.mimetype = 'application/json'
    return response 