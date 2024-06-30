from flask import Blueprint, request
from flask import current_app as app
from flask_jwt_extended import jwt_required, get_jwt

from ...utilities.responseHelper import bad_request, success, success_data
from .models import CategoryModels


# BLUEPRINT ============================================================ Begin
category = Blueprint(
    name='category',
    import_name=__name__,
    url_prefix='/category'
)
# BLUEPRINT ============================================================ End


# CREATE CATEGORY ============================================================ Begin
# POST https://127.0.0.1:5000/category/
@category.post('/')
@jwt_required()
def create_data():
    try:
        # Access User ======================================== 
        id = str(get_jwt()["id"])
        role = str(get_jwt()["role"])

        # Request Data ======================================== 
        data = request.json

        # Request Process ======================================== 
        response = CategoryModels.add_category(id, role, data)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# CREATE CATEGORY ============================================================ End


# GET CATEGORY ============================================================ Begin
# GET https://127.0.0.1:5000/category/
@category.get('/')
def get_data():
    try:
        # Request Process ======================================== 
        response = CategoryModels.view_category()

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# GET CATEGORY ============================================================ End


# UPDATE CATEGORY ============================================================ Begin
# PUT https://127.0.0.1:5000/category/
@category.put('/')
@jwt_required()
def update_data():
    try:
        # Access User ======================================== 
        id = str(get_jwt()["id"])
        role = str(get_jwt()["role"])

        # Request Data ======================================== 
        data = request.json

        # Request Process ======================================== 
        response = CategoryModels.edit_category(id, role, data)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# UPDATE CATEGORY ============================================================ End


# DELETE CATEGORY ============================================================ Begin
# DELETE https://127.0.0.1:5000/category/
@category.delete('/')
@jwt_required()
def delete_data():
    try:
        # Access User ======================================== 
        id = str(get_jwt()["id"])
        role = str(get_jwt()["role"])

        # Request Data ======================================== 
        data = request.args

        # Request Process ======================================== 
        response = CategoryModels.delete_category(id, role, data)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# DELETE CATEGORY ============================================================ End


# GET DETAIL CATEGORY ============================================================ Begin
# GET https://127.0.0.1:5000/category/detail
@category.get('/detail')
@jwt_required()
def detail_data():
    try:
        # Request Data ======================================== 
        data = request.args

        # Request Process ======================================== 
        response = CategoryModels.view_detail_category(data)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# GET DETAIL CATEGORY ============================================================ End


# GET COUNT CATEGORY ============================================================ Begin
# GET https://127.0.0.1:5000/category/count
@category.get('/count')
@jwt_required()
def count_data():
    try:
        # Request Process ======================================== 
        response = CategoryModels.get_count_category()

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# GET COUNT CATEGORY ============================================================ End
