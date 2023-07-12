from flask_jwt_extended import create_access_token

from ...utilities.responseHelper import invalid_params, parameter_error, defined_error, bad_request, success, success_data
from ...utilities.dbHelper import DBHelper
from ...utilities.queries import ADM_ADD_QUERY
from ...utilities.validator import vld_admin_regis, vld_signin
from ...utilities.utils import hashPassword

import time

# BLOCK FIRST/BASE ============================================================ Begin
class AdminModels():
    # CREATE ADMIN ============================================================ Begin
    def create_admin(datas):
        try:
            if datas == None:
                return invalid_params()
            
            requiredData = ["name", "email", "password", "retype_password"]
            for req in requiredData:
                if req not in datas:
                    return parameter_error(f"Missing {req} in Request Body")
            
            # Initialize Data ---------------------------------------- Start
            name = datas["name"].strip().title()
            email = datas["email"].strip().lower()
            password = datas["password"].strip()
            retypePassword = datas["retype_password"].strip()
            # Initialize Data ---------------------------------------- Finish

            # Data Validation ---------------------------------------- Start
            checkResult = vld_admin_regis(name, email, password, retypePassword)
            if len(checkResult) != 0:
                return defined_error(checkResult, "Bad Request", 400)
            # Data Validation ---------------------------------------- Finish
            
            # Insert Data ---------------------------------------- Start
            passEncrypt = hashPassword(password)
            timestamp = int(round(time.time()*1000))
            query = ADM_ADD_QUERY
            values = (name, email, passEncrypt, timestamp, timestamp)
            DBHelper().save_data(query, values)
            # Insert Data ---------------------------------------- Finish

            # Return Response ======================================== 
            return success("Successed!")

        except Exception as e:
            return bad_request(str(e))
    # CREATE ADMIN ============================================================ End

    # SIGN IN ============================================================ Begin
    def signin_admin(datas):
        try:
            if datas == None:
                return invalid_params()
            
            requiredData = ["email", "password"]
            for req in requiredData:
                if req not in datas:
                    return parameter_error(f"Missing {req} in Request Body")
                
            email = datas["email"].strip().lower()
            password = datas["password"].strip()
            
            # Data Validation ---------------------------------------- Start
            checkResult, result = vld_signin(email, password)
            if len(checkResult) != 0:
                return defined_error(checkResult, "Bad Request", statusCode=400)
            # Data Validation ---------------------------------------- Finish
            
            # Create jwt_payload
            jwt_payload = {
                "id" : result[0]["id"],
                "email" : email,
                "nama" : result[0]["name"]
            }
            
            # Create access_token by email & jwt_payload
            access_token = create_access_token(email, additional_claims=jwt_payload)

            # Insert access_token to jwt_payload
            jwt_payload["access_token"] = access_token

            response = {
                "access_token" : access_token,
                "role" : "ADMIN"
            }

            # Send success response
            return success_data("Sign In Successed.", response)

        except Exception as e:
            return bad_request(str(e))
    # SIGN IN ============================================================ End

    # VIEW PROFILE ============================================================ Begin
    def view_profile_admin(datas):
        try:
            if datas == None:
                return invalid_params()
            
            requiredData = ["email", "password"]
            for req in requiredData:
                if req not in datas:
                    return parameter_error(f"Missing {req} in Request Body")
            
        except Exception as e:
            return bad_request(str(e))
    # VIEW PROFILE ============================================================ End
# BLOCK FIRST/BASE ============================================================ End