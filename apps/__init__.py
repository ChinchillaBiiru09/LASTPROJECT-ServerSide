from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

from .confgure import config
from .confgure.connectionDB import ConnectDB

# =================================== CONFIG ===================================
app = Flask(__name__)
app.config['PRODUCT_ENVIRONMENT'] = config.PRODUCT_ENVIRONMENT

# App URL
app.config['BASE_URL'] = config.BASE_URL
app.config['FE_URL'] = os.getenv("FRONTEND_URL")

# Config JWT
app.config['SECRET_KEY'] = config.JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRED'] = config.JWT_ACCESS_TOKEN_EXPIRED
jwt = JWTManager(app)

# Config Database Migration
app.config.from_object(ConnectDB)
# app.config['db'] = SQLAlchemy(app)
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

# Create Folder (if doesn't exist)
list_folder_to_create = [
    app.config['ADMIN_PHOTOS'],
]

for x in list_folder_to_create:
    if os.path.exists(x) == False:
        os.makedirs(x)

# =================================== DATABASE MODEL ===================================
from .database import adminDB
from .database import userDB

# =================================== CONFIG ===================================
@app.route('/')
def index():
    return 'TA Backend API Gateway - Version 1.0 - Development'

# =================================== CONFIG ===================================
# import blueprint here
from .routes.Admin.controller import admin
from .routes.User.controller import user

# Set Limiter Every Route
# limiter.limit("5/minute;12/hours")(admin)

# Register Blueprint Here
app.register_blueprint(admin)
app.register_blueprint(user)