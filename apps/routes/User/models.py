from flask_jwt_extended import create_access_token
from flask import current_app as app
from datetime import datetime

from ...utilities.responseHelper import invalid_params, parameter_error, defined_error, bad_request, success, success_data
from ...utilities.dbHelper import DBHelper
from ...utilities.queries import *
from ...utilities.utils import hashPassword
from ...utilities.validator import vld_user_regis, vld_signin, vld_role

import time, jwt

# USER MODELS ============================================================ Begin
class UserModels():
    # CREATE USER ============================================================ Begin
    def create_user(datas):
        try:
            # Validation Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            requiredData = ["first_name", "middle_name", "last_name", "phone_number", "email", "password", "retype_password"]
            for req in requiredData:
                if req not in datas:
                    return parameter_error(f"Missing {req} in Request Body")
            # Validation Request Body ---------------------------------------- Finish
            
            # Initialize Data ---------------------------------------- Start
            firstName = datas["first_name"]
            middleName = datas["middle_name"]
            lastName = datas["last_name"]
            phone = datas["phone_number"].strip()
            email = datas["email"].strip().lower()
            password = datas["password"].strip()
            retypePassword = datas["retype_password"].strip()
            # Initialize Data ---------------------------------------- Finish

            # Data Validation ---------------------------------------- Start
            checkResult = vld_user_regis(firstName, middleName, lastName, phone, email, password, retypePassword)
            if len(checkResult) != 0:
                return defined_error(checkResult, "Bad Request", statusCode=400)
            # Data Validation ---------------------------------------- Finish
            
            # Insert Data ---------------------------------------- Start
            passEncrypt = hashPassword(password)
            timestamp = int(round(time.time()*1000))
            query = USR_ADD_QUERY
            values = (firstName, email, passEncrypt, timestamp, timestamp, timestamp)
            resReturn = DBHelper().save_return(query, values)
            if resReturn == None:
                return defined_error("Gagal menyimpan data.", "Bad Request", 400)
            # Insert Data ---------------------------------------- Finish

            # Insert Profile ---------------------------------------- Start
            userId = resReturn
            level = 2  # 1:Admin, 2:User
            query = PROF_ADD_QUERY
            values = (userId, level, firstName, middleName, lastName, phone, 0, timestamp, timestamp)
            DBHelper().save_data(query, values)
            # Insert Profile ---------------------------------------- Finish

            # Log Activity Record ---------------------------------------- Start
            activity = f"User baru dengan id {userId} telah berhasil mendaftar."
            query = LOG_ADD_QUERY
            values = (userId, activity, )
            DBHelper().save_data(query, values)
            # Log Activity Record ---------------------------------------- Finish

            # Return Response ======================================== 
            return success("Succeed!")

        except Exception as e:
            return bad_request(str(e))
    # CREATE USER ============================================================ End

    # SIGN IN ============================================================ Begin
    def signin_user(datas):
        try:
            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            requiredData = ["email", "password"]
            for req in requiredData:
                if req not in datas:
                    return parameter_error(f"Missing {req} in Request Body")
            # Checking Request Body ---------------------------------------- Finish
            
            # Initialize Data Request ---------------------------------------- Start
            email = datas["email"].strip().lower()
            password = datas["password"].strip()
            # Initialize Data Request ---------------------------------------- Finish
            
            # Data Validation ---------------------------------------- Start
            checkResult, result, stts = vld_signin(email, password, "USER")
            if len(checkResult) != 0:
                return defined_error(checkResult, "Bad Request", statusCode=stts)
            # Data Validation ---------------------------------------- Finish
            
            # Data Payload ---------------------------------------- Start
            jwt_payload = {
                "id" : result[0]["id"],
                "email" : email,
                "name" : result[0]["username"]
            }
            # Data Payload ---------------------------------------- Finish

            # Access Token by Email ======================================== 
            access_token = create_access_token(email, additional_claims=jwt_payload)

            # Data Response ---------------------------------------- Start
            response = {
                "access_token" : access_token,
                "role" : "USER"
            }
            # Data Response ---------------------------------------- Finish

            # Return Response ======================================== 
            return success_data("Sign In Succeed.", response)

        except Exception as e:
            return bad_request(str(e))
    # SIGN IN ============================================================ End
        
    # GET ALL USER ============================================================ Begin
    def view_user(user_id, user_role):
        try:
            # Access Validation ---------------------------------------- Start
            access, message = vld_role(user_role)
            if not access:
                return defined_error(message, "Forbidden", 403)
            # Access Validation ---------------------------------------- Finish

            # Checking Data ---------------------------------------- Start
            query = USR_GET_QUERY
            result = DBHelper().execute(query)
            if len(result) == 0 or result == None:
                return defined_error("Belum ada data user.", "Bad Request", 400)
            # Checking Data ---------------------------------------- Finish

            # Response Data ---------------------------------------- Start
            response = []
            for rsl in result:
                data = {
                    "user_id" : rsl["id"],
                    "username" : rsl["username"],
                    "status" : "Active" if rsl["is_delete"] == 0 else "Blocked",                    
                    "last_active": datetime.fromtimestamp(rsl["created_at"]/1000)
                }
                response.append(data)
            # Response Data ---------------------------------------- Finish
            
            # Return Response ======================================== 
            return success_data("Succeed!", response)
        
        except Exception as e:
            return bad_request(str(e))
    # GET ALL USER ============================================================ End
# USER MODELS ============================================================ End
