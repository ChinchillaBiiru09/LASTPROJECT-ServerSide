from flask import Blueprint, request
from flask import current_app as app
from flask_jwt_extended import jwt_required, get_jwt

from ...utilities.responseHelper import bad_request
from .models import GreetingModels


# BLUEPRINT ============================================================ Begin
greeting = Blueprint(
    name='greeting',
    import_name=__name__,
    url_prefix='/greeting'
)
# BLUEPRINT ============================================================ End


# CREATE GREETING ============================================================ Begin
# POST https://127.0.0.1:5000/greeting/
@greeting.post('/')
def create_data():
    try:
        # Request Data ======================================== 
        data = request.json

        # Request Process ======================================== 
        response = GreetingModels.add_greeting(data)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# CREATE GREETING ============================================================ End


# GET GREETING ============================================================ Begin
# POST https://127.0.0.1:5000/greeting/
@greeting.get('/')
@jwt_required()
def get_data():
    try:
        # Access User ======================================== 
        id = str(get_jwt()["id"])
        role = str(get_jwt()["role"])
        
        # Request Data ======================================== 
        data = request.args

        # Request Process ======================================== 
        response = GreetingModels.view_greeting(id, role, data)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# GET GREETING ============================================================ End


# # GET GREETING ============================================================ Begin
# # GET https://127.0.0.1:5000/greeting/
# @greeting.get('/user/')
# @jwt_required()
# def get_data_by_user():
#     try:
#         # Access User ======================================== 
#         id = str(get_jwt()["id"])
#         role = str(get_jwt()["role"])

#         # Request Process ======================================== 
#         response = GreetingModels.view_all_greeting_by_user(id, role)

#         # Request Data ======================================== 
#         return response

#     except Exception as e:
#         return bad_request(str(e))
# # GET GREETING ============================================================ End


# GET DETAIL GREETING ============================================================ Begin
# GET https://127.0.0.1:5000/greeting/detail
@greeting.get('/detail')
@jwt_required()
def detail_data():
    try:
        # Access User ======================================== 
        id = str(get_jwt()["id"])
        role = str(get_jwt()["role"])

        # Request Data ======================================== 
        data = request.args

        # Request Process ======================================== 
        response = GreetingModels.view_detail_greeting(id, role, data)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# GET DETAIL GREETING ============================================================ End


# DELETE GREETING ============================================================ Begin
# DELETE https://127.0.0.1:5000/greeting/
@greeting.delete('/')
@jwt_required()
def delete_data():
    try:
        # Access User ======================================== 
        id = str(get_jwt()["id"])
        role = str(get_jwt()["role"])

        # Request Data ======================================== 
        data = request.json

        # Request Process ======================================== 
        response = GreetingModels.delete_greeting(id, role, data)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# DELETE GREETING ============================================================ End


# GET COUNT GREETING ============================================================ Begin
# GET https://127.0.0.1:5000/greeting/count
@greeting.get('/count')
@jwt_required()
def count_data():
    try:
        # Request Data ======================================== 
        id = str(get_jwt()["id"])

        # Request Process ======================================== 
        response = GreetingModels.get_count_greeting(id)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# GET COUNT GREETING ============================================================ End
