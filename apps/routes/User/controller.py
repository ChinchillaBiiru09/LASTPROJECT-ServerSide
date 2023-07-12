from flask import Blueprint, request, make_response, jsonify, current_app as pp
from flask_jwt_extended import jwt_required, get_jwt

from ...utilities.responseHelper import bad_request
from .models import UserModels

# BLUEPRINT ============================================================ Begin
user = Blueprint(
    name='user',
    import_name=__name__,
    url_prefix='/user'
)
# BLUEPRINT ============================================================ End


# REGISTER USER ============================================================ Begin
# POST https://127.0.0.1:5000/user/
@user.post('/')
def create():
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


# VIEW PROFILE USER ============================================================ Begin
# GET https://127.0.0.1:5000/user/profile
@user.get('/profile')
@jwt_required()
def profile():
    try:
        # Access User ======================================== 
        id = str(get_jwt()["id"])
        role = str(get_jwt()["role"])

        # Request Data ======================================== 
        data = request.json

        # Request Data ======================================== 
        response = UserModels.view_profile_user(id, role, data)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# VIEW PROFILE USER ============================================================ End


# EDIT PROFILE USER ============================================================ Begin
# PUT https://127.0.0.1:5000/user/profile/edit
@user.put('/profile/edit')
@jwt_required()
def update_data():
    try:
        # Access User ======================================== 
        id = str(get_jwt()["id"])
        role = str(get_jwt()["role"])
        
        # Request Data ======================================== 
        data = request.json

        # Request Data ======================================== 
        response = UserModels.view_profile_user(data)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# EDIT PROFILE USER ============================================================ End

