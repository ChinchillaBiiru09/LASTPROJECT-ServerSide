from flask import Blueprint, request
from flask import current_app as app
from flask_jwt_extended import jwt_required, get_jwt

from ...utilities.responseHelper import bad_request, success, success_data
from .models import GuestModels


# BLUEPRINT ============================================================ Begin
guest = Blueprint(
    name='guest',
    import_name=__name__,
    url_prefix='/guest'
)
# BLUEPRINT ============================================================ End


# CREATE GUEST ============================================================ Begin
# POST https://127.0.0.1:5000/guest/
@guest.post('/')
@jwt_required()
def create_data():
    try:
        # Access User ======================================== 
        id = str(get_jwt()["id"])
        role = str(get_jwt()["role"])

        # Request Data ======================================== 
        data = request.json

        # Request Process ======================================== 
        response = GuestModels.add_guest(id, role,  data)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# CREATE GUEST ============================================================ End


# GET GUEST ============================================================ Begin
# GET https://127.0.0.1:5000/guest/
@guest.get('/')
@jwt_required()
def get_data():
    try:
        # Access User ======================================== 
        id = str(get_jwt()["id"])
        role = str(get_jwt()["role"])

        # Request Data ======================================== 
        data = request.args

        # Request Process ======================================== 
        response = GuestModels.view_guest(id, role, data)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# GET GUEST ============================================================ End


# DELETE GUEST ============================================================ Begin
# DELETE https://127.0.0.1:5000/guest/
@guest.delete('/')
@jwt_required()
def delete_data():
    try:
        # Access User ======================================== 
        id = str(get_jwt()["id"])
        role = str(get_jwt()["role"])

        # Request Data ======================================== 
        data = request.args

        # Request Process ======================================== 
        response = GuestModels.delete_guest(id, role, data)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# DELETE GUEST ============================================================ End


# GET DETAIL GUEST ============================================================ Begin
# GET https://127.0.0.1:5000/guest/detail
@guest.get('/detail')
@jwt_required()
def detail_data():
    try:
        # Access User ======================================== 
        # id = str(get_jwt()["id"])
        role = str(get_jwt()["role"])
        
        # Request Data ======================================== 
        data = request.args

        # Request Process ======================================== 
        response = GuestModels.view_detail_guest(role, data)

        # Request Data ======================================== 
        return success_data(response)

    except Exception as e:
        return bad_request(str(e))
# GET DETAIL GUEST ============================================================ End


# GET DETAIL GUEST ============================================================ Begin
# GET https://127.0.0.1:5000/guest/detail
@guest.get('/detail/id')
@jwt_required()
def detail_by_id():
    try:        
        # Request Data ======================================== 
        data = request.args

        # Request Process ======================================== 
        response = GuestModels.view_guest_by_id(data)

        # Request Data ======================================== 
        return success_data(response)

    except Exception as e:
        return bad_request(str(e))
# GET DETAIL GUEST ============================================================ End


# GET COUNT GUEST ============================================================ Begin
# GET https://127.0.0.1:5000/guest/count
@guest.get('/count')
@jwt_required()
def count_data():
    try:
        # Request Data ======================================== 
        id = str(get_jwt()["id"])

        # Request Process ======================================== 
        response = GuestModels.get_count_guest(id)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# GET COUNT GUEST ============================================================ End
