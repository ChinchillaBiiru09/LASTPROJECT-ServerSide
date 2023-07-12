from flask_jwt_extended import create_access_token, decode_token

from ...utilities.responseHelper import invalid_params, parameter_error, defined_error, bad_request, success, success_data
from ...utilities.dbHelper import DBHelper
from ...utilities.queries import USR_ADD_QUERY, PROF_ADD_QUERY, PROF_GET_BY_ID_QUERY, PROF_UPDATE_QUERY
from ...utilities.utils import hashPassword
from ...utilities.validator import vld_user_regis, vld_signin, vld_role

import time

# BLOCK FIRST/BASE ============================================================ Begin
class UserModels():
    # CREATE ADMIN ============================================================ Begin
    def create_user(datas):
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
            checkResult = vld_user_regis(name, email, password, retypePassword)
            if len(checkResult) != 0:
                return defined_error(checkResult, "Bad Request", statusCode=400)
            # Data Validation ---------------------------------------- Finish
            
            # Insert Data ---------------------------------------- Start
            passEncrypt = hashPassword(password)
            timestamp = int(round(time.time()*1000))
            query = USR_ADD_QUERY
            values = (name, email, passEncrypt, timestamp, timestamp)
            DBHelper().save_data(query, values)
            # Insert Data ---------------------------------------- Finish

            # Return Response ======================================== 
            return success("Successed!")

        except Exception as e:
            return bad_request(str(e))
    # CREATE ADMIN ============================================================ End

    # SIGN IN ============================================================ Begin
    def signin_user(datas):
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
            checkResult, result, stts = vld_signin(email, password)
            if len(checkResult) != 0:
                return defined_error(checkResult, "Bad Request", statusCode=stts)
            # Data Validation ---------------------------------------- FinishUser12345
            
            # Create jwt_payload
            jwt_payload = {
                "id" : result[0]["id"],
                "email" : email,
                "name" : result[0]["name"],
                "role" : "USER"
            }
            
            # Create access_token by email & jwt_payload
            access_token = create_access_token(email, additional_claims=jwt_payload)

            # Insert access_token to jwt_payload
            jwt_payload["access_token"] = access_token

            # response = {
            #     "access_token" : access_token,
            #     "role" : "USER"
            # }

            # Send success response
            oke = success_data("Sign In Successed.", jwt_payload)
            print(oke)
            return oke

        except Exception as e:
            return bad_request(str(e))
    # SIGN IN ============================================================ End

    # VIEW PROFILE ============================================================ Begin
    def view_profile_user(user_id, user_role):
        try:
            # Set Level User ---------------------------------------- Start
            user_level = 1  # 1 = Admin
            access, message = vld_role(user_role)
            if not access:
                user_level = 2  # 2 = User
            # Set Level User ---------------------------------------- Finish
            
            # Get Data ---------------------------------------- Start
            query = PROF_GET_BY_ID_QUERY
            values = (user_id, user_level)
            result = DBHelper().get_data(query, values)
            if len(result) == 0 :
                return defined_error("Gagal menemukan data user.", "Bad Request", 400)
            # Get Data ---------------------------------------- Finish

            # Response Data ---------------------------------------- Start
            response = {
                "id" : result[0]["id"],
                "first_name" : result[0]["first_name"],
                "middle_name" : result[0]["middle_name"],
                "last_name" : result[0]["last_name"],
                "phone" : result[0]["phone"],
                "photos" : result[0]["photos"]
            }
            # Response Data ---------------------------------------- Finish

            # Return Response ======================================== 
            return success_data("Successed!", response)
            
        except Exception as e:
            return bad_request(str(e))
    # VIEW PROFILE ============================================================ End

    # VIEW PROFILE ============================================================ Begin
    def edit_profile_user(user_id, user_role, datas):
        try:
            if datas == None:
                return invalid_params()
            
            requiredData = []
            for req in requiredData:
                if req not in datas:
                    return parameter_error(f"Missing {req} in Request Body")
            
        except Exception as e:
            return bad_request(str(e))
    # VIEW PROFILE ============================================================ End
# BLOCK FIRST/BASE ============================================================ End
