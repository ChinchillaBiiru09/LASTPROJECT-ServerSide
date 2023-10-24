from flask import Blueprint, request
from flask import current_app as app
from flask_jwt_extended import jwt_required, get_jwt

from ...utilities.responseHelper import bad_request
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
# POST https://127.0.0.1:5000/category/
@category.get('/')
def get_all_data():
    try:
        # Request Process ======================================== 
        response = CategoryModels.view_category()

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# GET CATEGORY ============================================================ End


# UPDATE CATEGORY ============================================================ Begin
# POST https://127.0.0.1:5000/category/
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
# POST https://127.0.0.1:5000/category/
@category.delete('/')
@jwt_required()
def delete_data():
    try:
        # Access User ======================================== 
        id = str(get_jwt()["id"])
        role = str(get_jwt()["role"])

        # Request Data ======================================== 
        data = request.json

        # Request Process ======================================== 
        response = CategoryModels.delete_category(id, role, data)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# DELETE CATEGORY ============================================================ End


# VIEW DETAIL CATEGORY ============================================================ Begin
# POST https://127.0.0.1:5000/category/detail
@category.get('/detail')
@jwt_required()
def get_data():
    try:
        # Access User ======================================== 
        role = str(get_jwt()["role"])

        # Request Data ======================================== 
        data = request.json

        # Request Process ======================================== 
        response = CategoryModels.view_detail_category(role, data)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# VIEW DETAIL CATEGORY ============================================================ End
