from flask import Blueprint, request
from flask import current_app as app
from flask_jwt_extended import jwt_required, get_jwt

from ...utilities.responseHelper import bad_request, success, success_data
from .models import ReqTemplateModels


# BLUEPRINT ============================================================ Begin
reqtemp = Blueprint(
    name='reqtemp',
    import_name=__name__,
    static_folder = '../../static/request_template',
    static_url_path="/media",
    url_prefix='/template/request'
)
# BLUEPRINT ============================================================ End


# CREATE TEMPLATE ============================================================ Begin
# POST https://127.0.0.1:5000/template/request/
@reqtemp.post('/')
@jwt_required()
def create_data():
    try:
        # Access User ======================================== 
        id = str(get_jwt()["id"])
        role = str(get_jwt()["role"])

        # Request Data ======================================== 
        data = request.json

        # Request Process ======================================== 
        response = ReqTemplateModels.add_request_template(id, role, data)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# CREATE TEMPLATE ============================================================ End


# GET TEMPLATE ============================================================ Begin
# GET https://127.0.0.1:5000/template/request/
@reqtemp.get('/')
@jwt_required()
def get_data():
    try:
        # Access User ======================================== 
        id = str(get_jwt()["id"])
        role = str(get_jwt()["role"])

        # Request Process ======================================== 
        response = ReqTemplateModels.view_request_template(id, role)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# GET TEMPLATE ============================================================ End


# # UPDATE GUEST ============================================================ Begin
# # PUT https://127.0.0.1:5000/guest/
# @guest.put('/')
# @jwt_required()
# def update_data():
#     try:
#         # Access User ======================================== 
#         id = str(get_jwt()["id"])
#         role = str(get_jwt()["role"])

#         # Request Data ======================================== 
#         data = request.json

#         # Request Process ======================================== 
#         response = GuestModels.edit_guest(id, role,  data)

#         # Request Data ======================================== 
#         return response

#     except Exception as e:
#         return bad_request(str(e))
# # UPDATE GUEST ============================================================ End


# DELETE REQUEST ============================================================ Begin
# DELETE https://127.0.0.1:5000/guest/
@reqtemp.delete('/')
@jwt_required()
def delete_data():
    try:
        # Access User ======================================== 
        id = str(get_jwt()["id"])
        role = str(get_jwt()["role"])

        # Request Data ======================================== 
        data = request.args

        # Request Process ======================================== 
        response = ReqTemplateModels.delete_guest(id, role, data)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# DELETE REQUEST ============================================================ End


# GET TEMPLATE ============================================================ Begin
# GET https://127.0.0.1:5000/template/request/
@reqtemp.get('/detail')
@jwt_required()
def detail_data():
    try:
        # Access User ======================================== 
        id = str(get_jwt()["id"])
        role = str(get_jwt()["role"])

        # Request Data ======================================== 
        data = request.args

        # Request Process ======================================== 
        response = ReqTemplateModels.view_detail_request_template(id, role, data)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# GET TEMPLATE ============================================================ End
