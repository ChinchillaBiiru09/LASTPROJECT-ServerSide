from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address
import os

from .configure import config
from .configure.connectionDB import ConnectDB

# =================================== CONFIG ===================================
app = Flask(__name__)
app.config['PRODUCT_ENVIRONMENT'] = config.PRODUCT_ENVIRONMENT

# App URL
app.config['BASE_URL'] = config.BASE_URL
app.config['FE_URL'] = os.getenv("FRONTEND_URL")

# Config JWT
app.config['SECRET_KEY'] = config.JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = config.JWT_ACCESS_TOKEN_EXPIRES
jwt = JWTManager(app)

# Config Database Migration
app.config.from_object(ConnectDB)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Config request limiter
# limiter = Limiter(
#     app,
#     key_func=get_remote_address,
#     default_limits=["15/minute","35/hour"]
# )

# Config Folder Upload Here
app.config['ADMIN_PHOTOS'] = config.STATIC_FOLDER_PATH + "photos/admin/"
app.config['USER_PHOTOS'] = config.STATIC_FOLDER_PATH + "photos/user/"
app.config['TEMPLATE_THUMBNAIL_PHOTOS'] = config.STATIC_FOLDER_PATH + "templates/thumbnail/"
app.config['TEMPLATE_WALLPAPER_PHOTOS'] = config.STATIC_FOLDER_PATH + "templates/wallpaper/"
app.config['TEMPLATE_CSS_FILE'] = config.STATIC_FOLDER_PATH + "templates/css/"
app.config['TEMPLATE_JS_FILE'] = config.STATIC_FOLDER_PATH + "templates/js/"
app.config['USER_INVITATION_FILE'] = config.STATIC_FOLDER_PATH + "invitation/user/"

# Create Folder (if doesn't exist)
list_folder_to_create = [
    app.config['ADMIN_PHOTOS'],
    app.config['USER_PHOTOS'],
    app.config['TEMPLATE_THUMBNAIL_PHOTOS'],
    app.config['TEMPLATE_WALLPAPER_PHOTOS'],
    app.config['TEMPLATE_CSS_FILE'],
    app.config['TEMPLATE_JS_FILE'],
    app.config['USER_INVITATION_FILE'],
]

for x in list_folder_to_create:
    if os.path.exists(x) == False:
        os.makedirs(x)

# =================================== DATABASE MODEL ===================================
from .database import adminDB
from .database import userDB
from .database import profileDB
from .database import logDB
from .database import categoryDB
from .database import templateDB
from .database import invitationDB
from .database import guestDB
# from .database import testDB
from .database import greetingDB

# =================================== CONFIG ===================================
@app.route('/')
def index():
    return 'TA Backend Creavitation API Gateway - Version 1.0 - Development'

# =================================== CONFIG ===================================
# import blueprint here
from .routes.Admin.controller import admin
from .routes.User.controller import user
from .routes.Category.controller import category
from .routes.Greeting.controller import greeting
from .routes.Template.controller import template
from .routes.Profile.controller import profile
from .routes.Invitation.controller import invitation
from .routes.Guest.controller import guest
# from .routes.tester.controller import test

# Set Limiter Every Route
# limiter.limit("5/minute;12/hours")(admin)

# Register Blueprint Here
app.register_blueprint(admin)
app.register_blueprint(user)
app.register_blueprint(category)
app.register_blueprint(greeting)
app.register_blueprint(template)
app.register_blueprint(profile)
app.register_blueprint(invitation)
app.register_blueprint(guest)
# app.register_blueprint(testDB)
