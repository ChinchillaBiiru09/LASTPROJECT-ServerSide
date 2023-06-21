from flask import Blueprint, request, make_response, jsonify
from flask import current_app as app
from flask_jwt_extended import create_access_token


admin = Blueprint(
    name='admin',
    import_name=__name__,
    url_prefix='/admin'
)

@admin.post('/')
def admin_register():
    return "success:)"

@admin.post('/login')
def admin_login():
    return "success:)"
