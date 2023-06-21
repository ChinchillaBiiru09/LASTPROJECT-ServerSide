from flask import jsonify, make_response

def success(message, statusCode=200):
    return make_response(jsonify({"statusCode":statusCode, "message":message}), True)

def success_data(message, data, statusCode=200):
    return make_response(jsonify({"statusCode":statusCode, "message":message, "data":data}), True)

def not_found(message, statusCode=404):
    return make_response(jsonify({"statusCode":statusCode, "error":"Not Found", "message":message}), False)

def defined_error(message, error="Defined Error", statusCode=499):
    return make_response(jsonify({"statusCode":statusCode, "error":error, "message":message}), False)

def authorization_error():
    return make_response(jsonify({"statusCode":403, "error":"Permission Denied"}), False)

def invalid_params():
    return make_response(jsonify({"statusCode":400, "error":"Invalid Parameters"}), False)

def bad_request(description="", error="Bad Request", statusCode=400):
    return make_response(jsonify({"statusCode":statusCode, "error":error, "description":f"{description}"}), False)
