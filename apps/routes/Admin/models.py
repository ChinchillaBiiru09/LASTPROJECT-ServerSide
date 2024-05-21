from flask_jwt_extended import create_access_token
from flask import current_app as app
from datetime import datetime

from ...utilities.responseHelper import invalid_params, parameter_error, defined_error, bad_request, success, success_data
from ...utilities.dbHelper import DBHelper
from ...utilities.queries import *
from ...utilities.validator import vld_admin_regis, vld_signin
from ...utilities.utils import hashPassword

import time, jwt

# BLOCK FIRST/BASE ============================================================ Begin
class AdminModels():
    # CREATE ADMIN ============================================================ Begin
    def create_admin(datas):
        try:
            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            requiredData = ["username", "email", "password", "retype_password"]
            for req in requiredData:
                if req not in datas:
                    return parameter_error(f"Missing {req} in Request Body")
            # Checking Request Body ---------------------------------------- Finish
            
            # Initialize Data ---------------------------------------- Start
            username = datas["username"].strip()
            email = datas["email"].strip().lower()
            password = datas["password"].strip()
            retypePassword = datas["retype_password"].strip()
            # Initialize Data ---------------------------------------- Finish

            # Data Validation ---------------------------------------- Start
            checkResult = vld_admin_regis(username, email, password, retypePassword)
            if len(checkResult) != 0:
                return defined_error(checkResult, "Bad Request", 400)
            # Data Validation ---------------------------------------- Finish
            
            # Insert Data ---------------------------------------- Start
            passEncrypt = hashPassword(password)
            timestamp = int(round(time.time()*1000))
            query = ADM_ADD_QUERY
            values = (username, email, passEncrypt, timestamp, timestamp)
            resReturn = DBHelper().save_return(query, values)
            if resReturn == None:
                return defined_error("Gagal menyimpan data.", "Bad Request", 400)
            # Insert Data ---------------------------------------- Finish

            # Insert Profile ---------------------------------------- Start
            userId = resReturn
            level = 1  # 1:Admin, 2:User
            query = PROF_ADD_QUERY
            values = (userId, level, username, "", "", "", 0, timestamp, timestamp)
            DBHelper().save_data(query, values)
            # Insert Profile ---------------------------------------- Finish
            
            # Log Activity Record ---------------------------------------- Start
            activity = f"Admin baru dengan id {userId} telah berhasil ditambahkan."
            query = LOG_ADD_QUERY
            values = (userId, activity, )
            DBHelper().save_data(query, values)
            # Log Activity Record ---------------------------------------- Finish

            # Return Response ======================================== 
            return success("Succeed!")

        except Exception as e:
            return bad_request(str(e))
    # CREATE ADMIN ============================================================ End

    # SIGN IN ============================================================ Begin
    def signin_admin(datas):
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
            checkResult, result, stts = vld_signin(email, password, "ADMIN")
            if len(checkResult) != 0:
                return defined_error(checkResult, "Bad Request", statusCode=stts)
            # Data Validation ---------------------------------------- Finish
            
            # Data Payload ---------------------------------------- Start
            jwt_payload = {
                "id" : result[0]["id"],
                "email" : email,
                "name" : result[0]["name"],
                "role" : "ADMIN"
            }
            # Data Payload ---------------------------------------- Finish
            
            # Access Token by Email ======================================== 
            access_token = create_access_token(email, additional_claims=jwt_payload)
            
            # Data Response ---------------------------------------- Start
            response = {
                "access_token" : access_token,
                "role" : "ADMIN"
            }
            # Data Response ---------------------------------------- Finish
            
            # Return Response ======================================== 
            return success_data("Sign In Succeed.", response)

        except Exception as e:
            return bad_request(str(e))
    # SIGN IN ============================================================ End
# BLOCK FIRST/BASE ============================================================ End