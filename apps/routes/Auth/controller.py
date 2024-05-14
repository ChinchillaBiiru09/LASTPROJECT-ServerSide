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
@auth.get('/')
def get_all_data():
    try:
        # Request Process ======================================== 
        response = AuthModels.view_auth()

        # Request Data ======================================== 
        return response

    except Exception as e:
        return bad_request(str(e))
# GET CATEGORY ============================================================ End