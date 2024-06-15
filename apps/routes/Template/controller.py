from flask import Blueprint, request
from flask import current_app as app
from flask_jwt_extended import jwt_required, get_jwt

from ...utilities.responseHelper import bad_request
from .models import TemplateModels


# BLUEPRINT ============================================================ Begin
template = Blueprint(
    name='template',
    import_name=__name__,
    static_folder = '../../static/templates',
    static_url_path="/media",
    url_prefix='/template'
)
# BLUEPRINT ============================================================ End


# CREATE TEMPLATE ============================================================ Begin
# POST https://127.0.0.1:5000/template/
@template.post('/')
@jwt_required()
def create_data():
    try:
        # Access User ======================================== 
        id = str(get_jwt()["id"])
        role = str(get_jwt()["role"])

        # Request Data ======================================== 
        data = request.json

        # Request Process ======================================== 
        response = TemplateModels.add_template(id, role, data)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# CREATE TEMPLATE ============================================================ End


# GET TEMPLATE ============================================================ Begin
# GET https://127.0.0.1:5000/template/
@template.get('/')
def get_data():
    try:
        # Request Process ======================================== 
        response = TemplateModels.view_template()

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# GET TEMPLATE ============================================================ End


# UPDATE TEMPLATE ============================================================ Begin
# PUT https://127.0.0.1:5000/template/
@template.put('/')
@jwt_required()
def update_data():
    try:
        # Access User ======================================== 
        id = str(get_jwt()["id"])
        role = str(get_jwt()["role"])

        # Request Data ======================================== 
        data = request.json

        # Request Process ======================================== 
        response = TemplateModels.edit_template(id, role, data)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# UPDATE TEMPLATE ============================================================ End


# DELETE TEMPLATE ============================================================ Begin
# DELETE https://127.0.0.1:5000/template/
@template.delete('/')
@jwt_required()
def delete_data():
    try:
        # Access User ======================================== 
        id = str(get_jwt()["id"])
        role = str(get_jwt()["role"])

        # Request Data ======================================== 
        data = request.json

        # Request Process ======================================== 
        response = TemplateModels.delete_template(id, role, data)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# DELETE TEMPLATE ============================================================ End


# GET DETAIL TEMPLATE ============================================================ Begin
# GET https://127.0.0.1:5000/template/detail
@template.get('/detail')
@jwt_required()
def detail_data():
    try:
        # Request Data ======================================== 
        data = request.json

        # Request Process ======================================== 
        response = TemplateModels.view_detail_template(data)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# GET DETAIL TEMPLATE ============================================================ End


# VIEW TEMPLATE ============================================================ Begin
# GET https://127.0.0.1:5000/template/detail
@template.get('/show')
@jwt_required()
def show():
    try:
        # Request Data ======================================== 
        data = request.json

        # Request Process ======================================== 
        response = TemplateModels.view_detail_template(data)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# VIEW TEMPLATE ============================================================ End


# GET COUNT TEMPLATE ============================================================ Begin
# GET https://127.0.0.1:5000/template/detail
@template.get('/count')
@jwt_required()
def count_data():
    try:
        # Request Process ======================================== 
        response = TemplateModels.get_count_template()

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# GET COUNT TEMPLATE ============================================================ End
