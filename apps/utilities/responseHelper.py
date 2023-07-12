from flask import jsonify, make_response

def success(message, statusCode=200):
    return make_response(jsonify({"statusCode":statusCode, "message":message}), statusCode)

def success_data(message, data, statusCode=200):
    return make_response(jsonify({"statusCode":statusCode, "message":message, "data":data}), statusCode)

def not_found(message, statusCode=404):
    return make_response(jsonify({"statusCode":statusCode, "error":"Not Found", "message":message}), 404)

def defined_error(message, error="Defined Error", statusCode=499):
    return make_response(jsonify({"statusCode":statusCode, "error":error, "message":message}), statusCode)

def parameter_error(message, error="Parameter Error", statusCode=400):
    return make_response(jsonify({"statusCode":statusCode, "erro":error, "message":message}), statusCode)

def authorization_error():
    return make_response(jsonify({"statusCode":403, "error":"Permission Denied"}), 403)

def invalid_params():
    return make_response(jsonify({"statusCode":400, "error":"Invalid Parameters"}), 400)

def bad_request(description="", error="Bad Request", statusCode=400):
    return make_response(jsonify({"statusCode":statusCode, "error":error, "description":f"{description}"}), 400)
