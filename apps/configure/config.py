import os
import datetime
from dotenv import load_dotenv

# Read .env file
load_dotenv()

# Environment Config
PRODUCT_ENVIRONMENT = os.getenv("PRODUCT_ENVIRONMENT")
BASE_URL = os.getenv("BASE_URL")

# App Port Config
PORT = os.getenv("PORT")

# Database Config
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PWD  = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

# JWT Config
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=3)

# TWILIO WHATSAPP API
ACCOUNT_SID = os.getenv("ACCOUNT_SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")

# Folder Config
STATIC_FOLDER_PATH = os.path.abspath(os.path.join(__file__, "../../static")) + "/"
