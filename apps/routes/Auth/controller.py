from flask import Blueprint, request
from flask import current_app as app
from flask_jwt_extended import jwt_required, get_jwt

from ...utilities.responseHelper import bad_request
from .models import AuthModels


# BLUEPRINT ============================================================ Begin
auth = Blueprint(
    name='auth',
    import_name=__name__,
    url_prefix='/auth'
)
# BLUEPRINT ============================================================ End


# CREATE CATEGORY ============================================================ Begin
# POST https://127.0.0.1:5000/auth/
@auth.post('/')
def create_data():
    try:
        # Request Data ======================================== 
        data = request.json

        # Request Process ======================================== 
        response = AuthModels.create_auth(data)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# CREATE CATEGORY ============================================================ End


# CREATE CATEGORY ============================================================ Begin
# POST https://127.0.0.1:5000/auth/
@auth.get('/')
def get_all_data():
    try:
        pass
        # # Request Process ======================================== 
        # response = AuthModels.view_auth()

        # # Request Data ======================================== 
        # return response

    except Exception as e:
        return bad_request(str(e))
# CREATE CATEGORY ============================================================ End


# CREATE CATEGORY ============================================================ Begin
# POST https://127.0.0.1:5000/auth/detail
@auth.get('/detail')
def detail_data():
    try:
        # Request Data ======================================== 
        data = request.args

        # Request Process ======================================== 
        response = AuthModels.view_detail_auth(data)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# CREATE CATEGORY ============================================================ End


# CREATE CATEGORY ============================================================ Begin
# PUT https://127.0.0.1:5000/auth/
@auth.put('/')
def update_data():
    try:
        # Request Data ======================================== 
        data = request.json

        # Request Process ======================================== 
        response = AuthModels.edit_auth(data)

        # Response Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# CREATE CATEGORY ============================================================ End
