from flask import Blueprint, request
from flask import current_app as app
from flask_jwt_extended import jwt_required

from ...utilities.responseHelper import bad_request
from .models import AdminModels


# BLUEPRINT ============================================================ Begin
admin = Blueprint(
    name='admin',
    import_name=__name__,
    static_folder = '../../static/photos/admin',
    static_url_path="/media",
    url_prefix='/admin'
)
# BLUEPRINT ============================================================ End


# REGISTER ADMIN ============================================================ Begin
# POST https://127.0.0.1:5000/admin/
@admin.post('/')
def create_data():
    try:
        # Request Data ======================================== 
        data = request.json

        # Request Data ======================================== 
        response = AdminModels.create_admin(data)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# REGISTER ADMIN ============================================================ End

# SIGN IN ADMIN ============================================================ Begin
# POST https://127.0.0.1:5000/admin/signin
@admin.post('/signin')
def signin():
    try:
        # Request Data ======================================== 
        data = request.json

        # Request Data ======================================== 
        response = AdminModels.signin_admin(data)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# SIGN IN ADMIN ============================================================ End

# VIEW PROFILE ADMIN ============================================================ Begin
# GET https://127.0.0.1:5000/admin/profile
@admin.get('/profile')
@jwt_required()
def profile():
    try:
        # Request Data ======================================== 
        data = request.json

        # Request Data ======================================== 
        response = AdminModels.view_profile_admin(data)

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# VIEW PROFILE ADMIN ============================================================ End

