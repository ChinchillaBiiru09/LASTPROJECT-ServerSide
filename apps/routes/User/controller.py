from flask import Blueprint, request, make_response, jsonify, current_app as pp
from flask_jwt_extended import create_access_token, jwt_required

user = Blueprint(
    name='user',
    import_name=__name__,
    url_prefix='/user'
)

@user.post('/')
def user_register():
    return "success:)"

@user.post('/login')
def user_login():
    return "success:)"

@user.post('/profile')
@jwt_required()
def user_profile():
    return "success:)"
