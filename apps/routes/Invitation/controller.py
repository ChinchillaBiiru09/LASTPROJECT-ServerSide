from flask import Blueprint, request
from flask import current_app as app
from flask_jwt_extended import jwt_required, get_jwt

from ...utilities.responseHelper import bad_request, success, success_data
from .models import InvitationModels


# BLUEPRINT ============================================================ Begin
invitation = Blueprint(
    name='invitation',
    import_name=__name__,
    static_folder = '../../static/invitation/user',
    static_url_path="/media",
    url_prefix='/invitation'
)
# BLUEPRINT ============================================================ End


# CREATE INVITATION ============================================================ Begin
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
# CREATE INVITATION ============================================================ End


# GET INVITATION ============================================================ Begin
# GET https://127.0.0.1:5000/invitation/
@invitation.get('/')
@jwt_required()
def get_data():
    try:
        # Access User ======================================== 
        id = str(get_jwt()["id"])
        role = str(get_jwt()["role"])
        
        # Request Data ======================================== 
        data = request.args

        # Request Process ======================================== 
        response = InvitationModels.view_invitation(id, role, data)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# GET INVITATION ============================================================ End


# UPDATE INVITATION ============================================================ Begin
# PUT https://127.0.0.1:5000/invitation/
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
# UPDATE INVITATION ============================================================ End


# DELETE INVITATION ============================================================ Begin
# DELETE https://127.0.0.1:5000/invitation/
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
# DELETE INVITATION ============================================================ End


# VIEW DETAIL INVITATION ============================================================ Begin
# GET https://127.0.0.1:5000/invitation/detail
@invitation.get('/detail')
@jwt_required()
def detail_data():
    try:
        # Access User ======================================== 
        role = str(get_jwt()["role"])

        # Request Data ======================================== 
        data = request.args

        # Request Process ======================================== 
        response = InvitationModels.view_detail_invitation(role, data)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# VIEW DETAIL INVITATION ============================================================ End


# VIEW ROW-COUNT INVITATION ============================================================ Begin
# GET https://127.0.0.1:5000/invitation/count
@invitation.get('/count')
@jwt_required()
def count_data():
    try:
        # Request Data ======================================== 
        id = str(get_jwt()["id"])
        role = str(get_jwt()["role"])

        # Request Process ======================================== 
        response = InvitationModels.get_count_invitation(id, role)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# VIEW ROW-COUNT INVITATION ============================================================ End


# VIEW ROW-COUNT INVITATION ============================================================ Begin
# GET https://127.0.0.1:5000/invitation/count
@invitation.get('/share')
# @jwt_required()
def share_data():
    try:
        # Request Data ======================================== 
        # id = str(get_jwt()["id"])
        # role = str(get_jwt()["role"])

        # Request Data ======================================== 
        data = request.json

        # Request Process ======================================== 
        response = InvitationModels.share_invitation(data)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# VIEW ROW-COUNT INVITATION ============================================================ End
