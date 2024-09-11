from flask_jwt_extended import create_access_token
from flask import request
from datetime import datetime

from ..Profile.models import ProfileModels
from ..Auth.models import AuthModels
from ...utilities.responseHelper import *
from ...utilities.dbHelper import DBHelper
from ...utilities.queries import *
from ...utilities.utils import hashPassword, split_date_time
from ...utilities.validator import vld_user_regis, vld_signin, vld_role

import time

# USER MODELS ============================================================ Begin
class UserModels():
    # CREATE USER ============================================================ Begin
    # Clear
    def create_user(datas):
        try:
            # Validation Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            requiredData = [
                "first_name", "middle_name", "last_name", "phone_number", 
                "email", "password", "retype_password"
                ]
            for req in requiredData:
                if req not in datas:
                    return parameter_error(f"Missing {req} in Request Body.")
            # Validation Request Body ---------------------------------------- Finish
            
            # Initialize Data Input ---------------------------------------- Start
            firstName = datas["first_name"]
            middleName = datas["middle_name"]
            lastName = datas["last_name"]
            phone = datas["phone_number"].strip()
            email = datas["email"].strip()
            password = datas["password"].strip()
            retypePassword = datas["retype_password"].strip()
            # Initialize Data Input ---------------------------------------- Finish

            # Data Validation ---------------------------------------- Start
            checkResult = vld_user_regis(firstName, middleName, lastName, 
                                         phone, email, password, retypePassword)
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
            try:
                data = {
                    "user_id": resReturn,
                    "level": 2, # 1 = Admin, 2 = User
                    "first_name": firstName, 
                    "middle_name": middleName, 
                    "last_name": lastName, 
                    "phone": phone
                }
                profile = ProfileModels.create_profile(data)
            except Exception as e:
                return bad_request(str(e))
            # Insert Profile ---------------------------------------- Finish
            
            # Insert Authentication ---------------------------------------- Start
            try:
                data = {
                    "user_id": resReturn,
                    "user_level": 2, # 1 = Admin, 2 = User
                    "email": email
                }
                print(data)
                auth = AuthModels.create_auth(data)
                print("auth - ", auth)
            except Exception as e:
                return bad_request(str(e))
            # Insert Authentication ---------------------------------------- Finish
            print("sc - ",auth.status_code)
            # Log Activity Record ---------------------------------------- Start
            if profile.status_code != 200:
                query = USR_DELETE_QUERY
                values = (timestamp, resReturn, resReturn, )
                DBHelper().save_data(query, values)
                
                return bad_request("Gagal membuat akun.")
            elif auth.status_code != 200:
                # Delete User
                query = USR_DELETE_QUERY
                values = (timestamp, resReturn, resReturn, )
                DBHelper().save_data(query, values)
                
                # Delete Profile
                query = PROF_DELETE_QUERY
                values = (timestamp, resReturn, )
                DBHelper().save_data(query, values)

                return bad_request("Gagal membuat akun. Silahkan gunakan email yang valid.")
            else:
                activity = f"User baru dengan id {resReturn} telah berhasil mendaftar."
                query = LOG_ADD_QUERY
                values = (resReturn, 2, activity, timestamp, )
                DBHelper().save_data(query, values)
            # Log Activity Record ---------------------------------------- Finish

            # Return Response ======================================== 
            return success(statusCode=201)

        except Exception as e:
            return bad_request(str(e))
    # CREATE USER ============================================================ End

    # SIGN IN ============================================================ Begin
    # Clear
    def signin_user(datas):
        try:
            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            requiredData = ["email", "password"]
            for req in requiredData:
                if req not in datas:
                    return parameter_error(f"Missing {req} in Request Body.")
            # Checking Request Body ---------------------------------------- Finish
            
            # Initialize Data Input ---------------------------------------- Start
            email = datas["email"].strip().lower()
            password = datas["password"].strip()
            # Initialize Data Input ---------------------------------------- Finish
            
            # Data Validation ---------------------------------------- Start
            level = 2
            checkResult, result, stts = vld_signin(email, password, level)
            if len(checkResult) > 0:
                return defined_error(checkResult, "Bad Request", statusCode=stts)
            # Data Validation ---------------------------------------- Finish

            # Update Data Last Active ---------------------------------------- Start
            timestamp = int(round(time.time()*1000))
            query = USR_UPDATE_ACTIVE_QUERY
            values = (timestamp, result[0]["id"])
            DBHelper().save_data(query, values)
            # Update Data Last Active ---------------------------------------- Finish
            
            # Log Activity Record ---------------------------------------- Start
            activity = f"User dengan id {result[0]['id']} telah berhasil log in."
            query = LOG_ADD_QUERY
            values = (result[0]["id"], level, activity, timestamp, )
            DBHelper().save_data(query, values)
            # Log Activity Record ---------------------------------------- Finish

            # Generate File URL ---------------------------------------- Start
            if len(result) >= 1:
                detailRequestURL = str(request.url).find('?')
                if detailRequestURL != -1:
                    index = detailRequestURL
                    request.url = request.url[:index]
            for item in result:
                item["photos"] = f"{request.url_root}user/media/{item['photos']}"
            # Generate File URL ---------------------------------------- Finish
            
            # Data Payload ---------------------------------------- Start
            jwt_payload = {
                "id" : result[0]["id"],
                "email" : email,
                "name" : result[0]["username"],
                "photos" : result[0]["photos"],
                "role" : "USER"
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
            return success_data(response)

        except Exception as e:
            return bad_request(str(e))
    # SIGN IN ============================================================ End
    
    # GET ALL USER ============================================================ Begin
    # Clear
    def view_user(user_id, user_role):
        try:
            # Access Validation ---------------------------------------- Start
            access = vld_role(user_role)
            if not access: # Access = True -> Admin
                return authorization_error()
            # Access Validation ---------------------------------------- Finish

            # Get Data User ---------------------------------------- Start
            query = USR_GET_ALL_QUERY
            result = DBHelper().execute(query)
            if len(result) < 1 or result is None:
                return not_found("Data user tidak dapat ditemukan.")
            # Get Data User ---------------------------------------- Finish

            # Get Data User ---------------------------------------- Start
            query1 = INV_GET_BY_USR_QUERY
            query2 = REQ_GET_BY_USER_QUERY
            # Get Data User ---------------------------------------- Finish

            # Response Data ---------------------------------------- Start
            response = []
            for rsl in result:
                print("=======================================")
                values = (rsl['id'], 2, )
                invitation = DBHelper().get_count_filter_data(query1, values)
                reqUser = DBHelper().get_count_filter_data(query2, values)
                lastActive = split_date_time(datetime.fromtimestamp(rsl["last_active"]/1000))
                data = {
                    "user_id" : rsl["id"],
                    "username" : rsl["username"],
                    "invitation_count" : invitation,
                    "request_count" : reqUser,
                    "status" : "Active" if rsl["is_delete"] == 0 else "Blocked",                    
                    "last_active": lastActive
                }
                response.append(data)
            # Response Data ---------------------------------------- Finish
            
            # Return Response ======================================== 
            return success_data(response)
        
        except Exception as e:
            return bad_request(str(e))
    # GET ALL USER ============================================================ End
    
    # DELETE USER ============================================================ Begin
    def activate_user(datas):
        try:
            print(datas)
            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            requiredData = ["user_id", "user_level", "token"]
            for req in requiredData:
                if req not in datas:
                    return parameter_error(f"Missing {req} in Request Body.")
            # Checking Request Body ---------------------------------------- Finish

            # Initialize Data Input ---------------------------------------- Start
            userId = datas["user_id"]
            userLevel = datas["user_level"]
            token = datas["token"]
            # Initialize Data Input ---------------------------------------- Finish

            # Checking Data ---------------------------------------- Start
            query = USR_GET_BY_ID_QUERY
            values = (userId,)
            result = DBHelper().get_count_filter_data(query, values)
            if result < 1:
                return not_found(f"Data user dengan id {userId} tidak dapat ditemukan.")
            # Checking Data ---------------------------------------- Finish

            # Delete Account ---------------------------------------- Start
            query = USR_ACTIVATED_ACCOUNT_QUERY
            values = (userId, )
            DBHelper().save_data(query, values)
            # Delete Account ---------------------------------------- Finish

            # Return Response ======================================== 
            return success(message="Activate!")
        
        except Exception as e:
            return bad_request(str(e))
    # DELETE USER ============================================================ End
    
    # DELETE USER ============================================================ Begin
    def delete_user(user_id, user_role, datas):
        try:
            # # Access Validation ---------------------------------------- Start
            # access = vld_role(user_role)
            # if not access: # Access = True -> Admin
            #     return authorization_error()
            # # Access Validation ---------------------------------------- Finish

            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            if "user_id" not in datas:
                return parameter_error("Missing 'user_id' in request body.")
            
            usrId = datas["user_id"]
            if usrId == "":
                return defined_error("Id user tidak boleh kosong.", "Defined Error", 499)
            # Checking Request Body ---------------------------------------- Finish

            # Checking Data ---------------------------------------- Start
            query = USR_GET_BY_ID_QUERY
            values = (user_id,)
            result = DBHelper().get_count_filter_data(query, values)
            if result < 1:
                return not_found(f"Data user dengan id {usrId} tidak dapat ditemukan.")
            # Checking Data ---------------------------------------- Finish

            # Delete Account ---------------------------------------- Start
            timestamp = int(round(time.time()*1000))
            query = USR_DELETE_QUERY
            values = (timestamp, user_id, usrId)
            DBHelper().save_data(query, values)
            # Delete Account ---------------------------------------- Finish

            # Delete Profile ---------------------------------------- Start
            query = PROF_DELETE_QUERY
            values = (timestamp, usrId)
            DBHelper().save_data(query, values)
            # Delete Profile ---------------------------------------- Finish

            # Delete Invitation & Guest ---------------------------------------- Start
            query = INV_GET_BY_USR_QUERY
            values = (user_id, )
            invitations = DBHelper().get_data(query, values)
            if len(invitations) > 0:
                query1 = INV_DELETE_QUERY
                query2 = GUEST_GET_BY_CODE_QUERY
                query3 = GUEST_DELETE_INV_QUERY
                for invite in invitations:
                    # Delete Invitation
                    delValues1 = (timestamp, user_id, invite['id'], )
                    DBHelper().save_data(query1, delValues1)

                    # Delete Guest
                    values = (invite['code'], )
                    guest = DBHelper().get_count_filter_data(query2, values)
                    if guest > 0:
                        delValues2 = (timestamp, user_id, invite['code'], )
                        DBHelper().save_data(query3, delValues2)
            # Delete Invitation & Guest ---------------------------------------- Finish

            # Delete Template Private ---------------------------------------- Start
            query = TMPLT_GET_BY_USER_QUERY
            values = (user_id, )
            templates = DBHelper().get_count_filter_data(query, values)
            if templates > 0:
                query = TMPLT_PRIV_DELETE_USER_QUERY
                values = (timestamp, user_id, user_id, )
                DBHelper().save_data(query, values)
            # Delete Template Private ---------------------------------------- Finish
            
            # Return Response ======================================== 
            return success(message="Deleted!")
        
        except Exception as e:
            return bad_request(str(e))
    # DELETE USER ============================================================ End
    
    # GET ROW-COUNT USER ============================================================ Begin
    # Clear
    def get_count_user():
        try:
            # Checking Data ---------------------------------------- Start
            query = USR_GET_ALL_QUERY
            result = DBHelper().get_count_data(query)
            if result < 1 or result is None :
                return not_found("User tidak dapat ditemukan.")
            # Checking Data ---------------------------------------- Finish
            
            # Response Data ---------------------------------------- Start
            response = {
                "user_count" : result
            }
            # Response Data ---------------------------------------- Finish

            # Return Response ======================================== 
            return success_data(response)
        
        except Exception as e:
            return bad_request(str(e))
    # GET ROW-COUNT USER ============================================================ End
# USER MODELS ============================================================ End
