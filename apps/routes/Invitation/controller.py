from flask import Blueprint, request
from flask import current_app as app
from flask_jwt_extended import jwt_required, get_jwt

from ...utilities.responseHelper import bad_request
from .models import InvitationModels


# BLUEPRINT ============================================================ Begin
invitation = Blueprint(
    name='invitation',
    import_name=__name__,
    url_prefix='/invitation'
)
# BLUEPRINT ============================================================ End


# CREATE CATEGORY ============================================================ Begin
# POST https://127.0.0.1:5000/invitation/
@invitation.post('/')
@jwt_required()
def create_data():
    try:
        # Access User ======================================== 
        id = str(get_jwt()["id"])
        role = str(get_jwt()["role"])

        # Request Data ======================================== 
        data = request.json

        # Request Process ======================================== 
        response = InvitationModels.add_invitation(id, role, data)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# CREATE CATEGORY ============================================================ End


# GET CATEGORY ============================================================ Begin
# POST https://127.0.0.1:5000/invitation/
@invitation.get('/')
def get_all_data():
    try:
        # Request Process ======================================== 
        response = InvitationModels.view_invitation()

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# GET CATEGORY ============================================================ End


# UPDATE CATEGORY ============================================================ Begin
# POST https://127.0.0.1:5000/invitation/
@invitation.put('/')
@jwt_required()
def update_data():
    try:
        # Access User ======================================== 
        id = str(get_jwt()["id"])
        role = str(get_jwt()["role"])

        # Request Data ======================================== 
        data = request.json

        # Request Process ======================================== 
        response = InvitationModels.edit_invitation(id, role, data)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# UPDATE CATEGORY ============================================================ End


# DELETE CATEGORY ============================================================ Begin
# POST https://127.0.0.1:5000/invitation/
@invitation.delete('/')
@jwt_required()
def delete_data():
    try:
        # Access User ======================================== 
        id = str(get_jwt()["id"])
        role = str(get_jwt()["role"])

        # Request Data ======================================== 
        data = request.json

        # Request Process ======================================== 
        response = InvitationModels.delete_invitation(id, role, data)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# DELETE CATEGORY ============================================================ End


# VIEW DETAIL CATEGORY ============================================================ Begin
# POST https://127.0.0.1:5000/invitation/detail
@invitation.get('/detail')
@jwt_required()
def get_data():
    try:
        # Access User ======================================== 
        role = str(get_jwt()["role"])

        # Request Data ======================================== 
        data = request.json

        # Request Process ======================================== 
        response = InvitationModels.view_detail_invitation(role, data)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# VIEW DETAIL CATEGORY ============================================================ End
