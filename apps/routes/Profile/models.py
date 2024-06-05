from flask import request
from ...utilities.responseHelper import *
from ...utilities.dbHelper import DBHelper
from ...utilities.queries import *
from ...utilities.validator import vld_role, vld_edit_profile

from datetime import datetime

import time, base64

# USER MODELS ============================================================ Begin
class ProfileModels():
    # CREATE PROFILE ============================================================ Begin
    def create_profile(datas):
        try:
            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            requiredData = ["user_id", "level", "first_name", "middle_name", "last_name", "phone"]
            for req in requiredData:
                if req not in datas:
                    return parameter_error(f"Missing {req} in Request Body.")
            # Checking Request Body ---------------------------------------- Finish
            
        except Exception as e:
            return bad_request(str(e))
    # CREATE PROFILE ============================================================ End

    # UPDATE PROFILE ============================================================ Begin
    def edit_profile(user_id, user_role, datas):
        try:
            # Set Level User ---------------------------------------- Start
            userLevel = 1  # 1 = Admin
            access = vld_role(user_role)
            if not access: # Access = True -> Admin
                userLevel = 2  # 2 = User
            # Set Level User ---------------------------------------- Finish

            # Validation Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            requiredData = ["first_name", "middle_name", "last_name", "phone", "photos"]
            for req in requiredData:
                if req not in datas:
                    return parameter_error(f"Missing {req} in Request Body.")
            # Validation Request Body ---------------------------------------- Finish
            
            # Initialize Data ---------------------------------------- Start
            fName = datas["first_name"].strip().title()
            mName = datas["middle_name"].strip().title()
            lName = datas["last_name"].strip().title()
            phone = datas["phone"].strip()
            photos = datas["photos"]
            # Initialize Data ---------------------------------------- Finish

            # Data Validation ---------------------------------------- Start
            checkResult, result = vld_edit_profile(user_id, userLevel, fName, mName, lName, phone)
            if len(checkResult) != 0:
                return defined_error(checkResult, "Bad Request", 400)
            # Data Validation ---------------------------------------- Finish

            # Check Data ---------------------------------------- Start
            if fName == "":
                fName = result[0]["first_name"]
            if mName == "":
                mName = result[0]["middle_name"]
            if lName == "":
                lName = result[0]["last_name"]
            if phone == "":
                phone = result[0]["phone"]
            base_64 = 0
            if (photos != "") or (photos != None):
                base_64 = base64.b64decode(photos)
            # Check Data ---------------------------------------- Finish
            
            # Insert Data ---------------------------------------- Start
            timestamp = int(round(time.time()*1000))
            query = PROF_UPDATE_QUERY
            values = (fName, mName, lName, phone, base_64, timestamp, user_id, userLevel)
            DBHelper().save_data(query, values)
            # Insert Data ---------------------------------------- Finish

            # Log Activity Record ---------------------------------------- Start
            level = "Admin" if userLevel == 1 else "User"
            activity = f"{level} dengan id {user_id} telah mengubah data profile."
            query = LOG_ADD_QUERY
            values = (user_id, activity, )
            DBHelper().save_data(query, values)
            # Log Activity Record ---------------------------------------- Finish

            # Return Response ======================================== 
            return success(message="Updated!")
            
        except Exception as e:
            return bad_request(str(e))
    # UPDATE PROFILE ============================================================ End

    # GET DETAIL PROFILE ============================================================ Begin
    # Clear
    def view_profile(user_id, user_role, datas):
        try:
            # Set Level User ---------------------------------------- Start
            userLevel = 1  # 1 = Admin
            access = vld_role(user_role)
            if not access: # Access = True -> Admin
                userLevel = 2  # 2 = User
            # Set Level User ---------------------------------------- Finish

            # Checking Request Body ---------------------------------------- Start
            if datas != None:            
                if "user_id" not in datas:
                    return parameter_error("Missing 'user_id' in request body.")
                
                user_id = datas["user_id"]
                userLevel = 2
                if user_id == "":
                    return defined_error("Id user tidak boleh kosong.", "Defined Error", 499)
            # Checking Request Body ---------------------------------------- Finish
            
            # Get Data From Profile ---------------------------------------- Start
            query = PROF_GET_BY_ID_QUERY
            values = (user_id, userLevel)
            result1 = DBHelper().get_data(query, values)
            if len(result1) < 1 or result1 is None:
                return not_found("Data user tidak dapat ditemukan.")
            # Get Data From Profile ---------------------------------------- Finish

            # Get Data From Account ---------------------------------------- Start
            query = ADM_GET_BY_ID_QUERY if userLevel == 1 else USR_GET_BY_ID_QUERY
            values = (user_id, )
            result2 = DBHelper().get_data(query, values)
            # Get Data From Account ---------------------------------------- Finish
            
            # Generate File URL ---------------------------------------- Start
            if len(result1) >= 1:
                detailRequestURL = str(request.url).find('?')
                if detailRequestURL != -1:
                    index = detailRequestURL
                    request.url = request.url[:index]
            for item in result1:
                if userLevel == 1:
                    item["photos"] = f"{request.url_root}profile/media/admin/{item['photos']}"
                else:
                    item["photos"] = f"{request.url_root}profile/media/user/{item['photos']}"
            # Generate File URL ---------------------------------------- Finish

            # Response Data ---------------------------------------- Start
            lastSignin = datetime.fromtimestamp(result2[0]['last_active']/1000)
            createdAt = datetime.fromtimestamp(result1[0]['created_at']/1000)
            updatedAt = datetime.fromtimestamp(result1[0]['updated_at']/1000)
            response = {
                "id" : result1[0]["id"],
                "username" : result2[0]["username"],
                "first_name" : result1[0]["first_name"],
                "middle_name" : result1[0]["middle_name"],
                "last_name" : result1[0]["last_name"],
                "email" : result2[0]["email"],
                "status" : "Active" if result1[0]["is_delete"] == 0 else "Blocked",                    
                "last_active": lastSignin,
                "created_at": createdAt, 
                "updated_at": updatedAt,
                "phone" : result1[0]["phone"],
                "photos" : result1[0]["photos"]
            }
            # Response Data ---------------------------------------- Finish

            # Return Response ======================================== 
            return success_data(response)
            
        except Exception as e:
            return bad_request(str(e))
    # GET DETAIL PROFILE ============================================================ End

    # GET DETAIL PROFILE ============================================================ Begin
    def get_photo_profile(user_id, user_role):
        try:
            # Set Level User ---------------------------------------- Start
            userLevel = 1  # 1 = Admin
            access = vld_role(user_role)
            if not access: # Access = True -> Admin
                userLevel = 2  # 2 = User
            # Set Level User ---------------------------------------- Finish
            
            # Get Data From Profile ---------------------------------------- Start
            query = PROF_GET_BY_ID_QUERY
            values = (user_id, userLevel)
            result1 = DBHelper().get_data(query, values)
            if len(result1) < 1 or result1 is None:
                return not_found("Data user tidak dapat ditemukan.")
            # Get Data From Profile ---------------------------------------- Finish

            # Get Data From Account ---------------------------------------- Start
            query = ADM_GET_BY_ID_QUERY if userLevel == 1 else USR_GET_BY_ID_QUERY
            values = (user_id, )
            result2 = DBHelper().get_data(query, values)
            # Get Data From Account ---------------------------------------- Finish

            # Response Data ---------------------------------------- Start
            photosBase64 = base64.b64encode(result1[0]["photos"]).decode('utf-8')
            createdAt = datetime.fromtimestamp(result1[0]['created_at']/1000)
            response = {
                "id" : result1[0]["id"],
                "first_name" : result1[0]["first_name"],
                "middle_name" : result1[0]["middle_name"],
                "last_name" : result1[0]["last_name"],
                "email" : result2[0]["email"],
                "phone" : result1[0]["phone"],
                "photos" : photosBase64,
                "created_at" : createdAt
            }
            # Response Data ---------------------------------------- Finish

            # Return Response ======================================== 
            return success_data(response)
            
        except Exception as e:
            return bad_request(str(e))
    # GET DETAIL PROFILE ============================================================ End
# USER MODELS ============================================================ End
