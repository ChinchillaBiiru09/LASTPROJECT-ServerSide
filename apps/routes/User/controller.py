from flask import Blueprint, request, make_response, jsonify, current_app as app
from flask_jwt_extended import jwt_required, get_jwt

from ...utilities.responseHelper import bad_request
from .models import UserModels

# BLUEPRINT ============================================================ Begin
user = Blueprint(
    name='user',
    import_name=__name__,
    static_folder = '../../static/photos/user',
    static_url_path="/media",
    url_prefix='/user'
)
# BLUEPRINT ============================================================ End


# REGISTER USER ============================================================ Begin
# POST https://127.0.0.1:5000/user/
@user.post('/')
def create_data():
    try:
        # Request Data ======================================== 
        data = request.json

        # Request Data ======================================== 
        response = UserModels.create_user(data)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# REGISTER USER ============================================================ End


# SIGN IN USER ============================================================ Begin
# POST https://127.0.0.1:5000/user/signin
@user.post('/signin')
def signin():
    try:
        # Request Data ======================================== 
        data = request.json

        # Request Data ======================================== 
        response = UserModels.signin_user(data)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# SIGN IN USER ============================================================ End


# GET USER ============================================================ Begin
# GET https://127.0.0.1:5000/user/
@user.get('/')
@jwt_required()
def get_data():
    try:
        # Request Data ======================================== 
        id = str(get_jwt()["id"])
        role = str(get_jwt()["role"])

        # Request Data ======================================== 
        response = UserModels.view_user(id, role)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# GET USER ============================================================ End


# GET USER ============================================================ Begin
# DELETE https://127.0.0.1:5000/user/activate
@user.put('/activate')
def active_data():
    try:
        # Request Data ======================================== 
        data = request.json

        # Request Data ======================================== 
        response = UserModels.activate_user(data)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# GET USER ============================================================ End


# GET USER ============================================================ Begin
# DELETE https://127.0.0.1:5000/user/
@user.delete('/')
@jwt_required()
def delete_data():
    try:
        print("MASUK SINI?")
        # Request Data ======================================== 
        id = str(get_jwt()["id"])
        role = str(get_jwt()["role"])

        # Request Data ======================================== 
        data = request.args

        # Request Data ======================================== 
        response = UserModels.delete_user(id, role, data)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# GET USER ============================================================ End


# GET USER ============================================================ Begin
# GET https://127.0.0.1:5000/user/count
@user.get('/count')
@jwt_required()
def count_data():
    try:
        # Request Data ======================================== 
        response = UserModels.get_count_user()

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# GET USER ============================================================ End
