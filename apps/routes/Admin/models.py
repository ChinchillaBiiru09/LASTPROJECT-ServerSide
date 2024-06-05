from flask_jwt_extended import create_access_token
from flask import current_app as app
from datetime import datetime


from ..Profile.models import ProfileModels
from ...utilities.responseHelper import *
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
                    return parameter_error(f"Missing {req} in Request Body.")
            # Checking Request Body ---------------------------------------- Finish
            
            # Initialize Data Input ---------------------------------------- Start
            username = datas["username"].strip()
            email = datas["email"].strip().lower()
            password = datas["password"].strip()
            retypePassword = datas["retype_password"].strip()
            # Initialize Data Input ---------------------------------------- Finish

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
            # resReturn = DBHelper().save_return(query, values)
            # if resReturn == None:
            #     return defined_error("Gagal menyimpan data.", "Bad Request", 400)
            # Insert Data ---------------------------------------- Finish

            # Insert Profile ---------------------------------------- Start
            try:
                data = {
                    "user_id": 0,
                    "level": 1, # 1 = Admin, 2 = User
                    "first_name": username, 
                    "middle_name": "", 
                    "last_name": "", 
                    "phone": 0
                }
                profile = ProfileModels().create_profile(data)
                print(profile)
            except Exception as e:
                return bad_request(str(e))
            # userId = resReturn
            # level = 1  
            # query = PROF_ADD_QUERY
            # values = (userId, level, username, "", "", "", 0, timestamp, timestamp)
            # DBHelper().save_data(query, values)
            # Insert Profile ---------------------------------------- Finish
            
            # Log Activity Record ---------------------------------------- Start
            # activity = f"Admin baru dengan id {userId} telah berhasil ditambahkan."
            # query = LOG_ADD_QUERY
            # values = (userId, activity, )
            # DBHelper().save_data(query, values)
            # Log Activity Record ---------------------------------------- Finish

            # Return Response ======================================== 
            return success(statusCode=201)

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
                    return parameter_error(f"Missing {req} in Request Body.")
            # Checking Request Body ---------------------------------------- Finish
            
            # Initialize Data Request ---------------------------------------- Start
            email = datas["email"].strip().lower()
            password = datas["password"].strip()
            # Initialize Data Request ---------------------------------------- Finish
            
            # Data Validation ---------------------------------------- Start
            level = 1
            checkResult, result, stts = vld_signin(email, password, level)
            if len(checkResult) != 0:
                return defined_error(checkResult, "Bad Request", statusCode=stts)
            # Data Validation ---------------------------------------- Finish

            # Update Data Last Active ---------------------------------------- Start
            timestamp = int(round(time.time()*1000))
            query = ADM_UPDATE_ACTIVE_QUERY
            values = (timestamp, result[0]["id"])
            DBHelper().save_data(query, values)
            # Update Data Last Active ---------------------------------------- Finish
            
            # Log Activity Record ---------------------------------------- Start
            activity = f"Admin dengan id {result[0]['id']} telah berhasil log in."
            query = LOG_ADD_QUERY
            values = (result[0]["id"], level, activity, )
            DBHelper().save_data(query, values)
            # Log Activity Record ---------------------------------------- Finish
            
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
            return success_data(response)

        except Exception as e:
            return bad_request(str(e))
    # SIGN IN ============================================================ End
# BLOCK FIRST/BASE ============================================================ End