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
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB

# App URL
app.config['BASE_URL'] = config.BASE_URL
app.config['FE_URL'] = os.getenv("FRONTEND_URL")

# Config JWT
app.config['SECRET_KEY'] = config.JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = config.JWT_ACCESS_TOKEN_EXPIRES
jwt = JWTManager(app)

# # API Whatsapp
# app.config['ACCOUNT_SID'] = config.ACCOUNT_SID
# app.config['AUTH_TOKEN'] = config.AUTH_TOKEN

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
app.config['DEFAULT_PHOTOS'] = config.STATIC_FOLDER_PATH + "photos/"
app.config['ADMIN_PHOTOS'] = config.STATIC_FOLDER_PATH + "photos/admin/"
app.config['USER_PHOTOS'] = config.STATIC_FOLDER_PATH + "photos/user/"
app.config['TEMPLATE_THUMBNAIL_PHOTOS'] = config.STATIC_FOLDER_PATH + "templates/thumbnail/"
app.config['TEMPLATE_WALLPAPER_PHOTOS'] = config.STATIC_FOLDER_PATH + "templates/wallpaper/"
app.config['TEMPLATE_CSS_FILE'] = config.STATIC_FOLDER_PATH + "templates/css/"
app.config['TEMPLATE_JS_FILE'] = config.STATIC_FOLDER_PATH + "templates/js/"
app.config['USER_INVITATION_FILE'] = config.STATIC_FOLDER_PATH + "invitation/user/"
app.config['GALLERY_INVITATION_FILE'] = config.STATIC_FOLDER_PATH + "invitation/gallery/"
app.config['TEMPLATE_REQUEST_DESIGN'] = config.STATIC_FOLDER_PATH + "request_template/"
app.config['EXPORT_GUEST'] = config.STATIC_FOLDER_PATH + "guest/export/"

# Create Folder (if doesn't exist)
list_folder_to_create = [
    app.config['ADMIN_PHOTOS'],
    app.config['USER_PHOTOS'],
    app.config['TEMPLATE_THUMBNAIL_PHOTOS'],
    app.config['TEMPLATE_WALLPAPER_PHOTOS'],
    app.config['TEMPLATE_CSS_FILE'],
    app.config['TEMPLATE_JS_FILE'],
    app.config['USER_INVITATION_FILE'],
    app.config['TEMPLATE_REQUEST_DESIGN'],
    app.config['GALLERY_INVITATION_FILE'],
    app.config['EXPORT_GUEST']
]

for x in list_folder_to_create:
    if os.path.exists(x) == False:
        os.makedirs(x)

# =================================== DATABASE MODEL ===================================
from .database import adminDB
from .database import authDB
from .database import userDB
from .database import profileDB
from .database import logDB
from .database import categoryDB
from .database import templateDB
from .database import invitationDB
from .database import guestDB
from .database import requserDB
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
from .routes.Log.controller import log
from .routes.Request.controller import reqtemp
from .routes.Auth.controller import auth
from .routes.tester.controller import test

# Register Blueprint Here
app.register_blueprint(admin)
app.register_blueprint(user)
app.register_blueprint(category)
app.register_blueprint(greeting)
app.register_blueprint(template)
app.register_blueprint(profile)
app.register_blueprint(invitation)
app.register_blueprint(guest)
app.register_blueprint(log)
app.register_blueprint(reqtemp)
app.register_blueprint(auth)
app.register_blueprint(test)


# Set Limiter Every Route
# limiter.limit("5/minute;12/hours")(admin)