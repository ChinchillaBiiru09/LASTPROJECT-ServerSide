from ...utilities.responseHelper import invalid_params, parameter_error, defined_error, bad_request, success, success_data
from ...utilities.dbHelper import DBHelper
from ...utilities.queries import *
from ...utilities.validator import vld_role, vld_invitation
from ...utilities.utils import random_number, saving_image, random_string_number

from flask import request, current_app as app
from werkzeug.utils import secure_filename

import time, os

class AuthModels():
    # GET AUTH ============================================================ Begin
    def view_auth():
        pass
    # GET AUTH ============================================================ End