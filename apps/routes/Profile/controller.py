from flask import Blueprint, request, make_response, jsonify, current_app as app
from flask_jwt_extended import jwt_required, get_jwt

from ...utilities.responseHelper import bad_request
from .models import ProfileModels

# BLUEPRINT ============================================================ Begin
profile = Blueprint(
    name='profile',
    import_name=__name__,
    static_folder = '../../static/photos', 
    static_url_path="/media",
    url_prefix='/profile'
)
# BLUEPRINT ============================================================ End


# VIEW PROFILE ============================================================ Begin
# GET https://127.0.0.1:5000/profile/
@profile.get('/')
@jwt_required()
def get_data():
    try:
        # Access User ======================================== 
        id = str(get_jwt()["id"])
        role = str(get_jwt()["role"])

        # Request Data ======================================== 
        data = request.args

        # Request Data ======================================== 
        response = ProfileModels.view_profile(id, role, data)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# VIEW PROFILE ============================================================ End


# EDIT PROFILE ============================================================ Begin
# PUT https://127.0.0.1:5000/profile/
@profile.put('/')
@jwt_required()
def update_data():
    try:
        # Access User ======================================== 
        id = str(get_jwt()["id"])
        role = str(get_jwt()["role"])
        
        # Request Data ======================================== 
        data = request.json

        # Request Data ======================================== 
        response = ProfileModels.edit_profile(id, role, data)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# EDIT PROFILE ============================================================ End
