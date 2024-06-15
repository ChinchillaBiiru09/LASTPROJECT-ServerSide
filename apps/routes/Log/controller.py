from flask import Blueprint, request
from flask import current_app as app
from flask_jwt_extended import jwt_required, get_jwt

from ...utilities.responseHelper import bad_request
from .models import LogModels


# BLUEPRINT ============================================================ Begin
log = Blueprint(
    name='log',
    import_name=__name__,
    url_prefix='/log'
)
# BLUEPRINT ============================================================ End


# GET LOG ============================================================ Begin
# GET https://127.0.0.1:5000/log/
@log.get('/')
@jwt_required()
def get_data():
    try:
        # Access User ======================================== 
        role = str(get_jwt()["role"])

        # Request Process ======================================== 
        response = LogModels.view_log(role)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# GET LOG ============================================================ End


# GET LOG ON PROFILE ============================================================ Begin
# GET https://127.0.0.1:5000/log/activity
@log.get('/activity')
@jwt_required()
def get_data_by_user():
    try:
        # Access User ======================================== 
        id = str(get_jwt()["id"])
        role = str(get_jwt()["role"])

        # Request Process ======================================== 
        response = LogModels.view_log_by_user(id, role)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# GET LOG ON PROFILE ============================================================ End
