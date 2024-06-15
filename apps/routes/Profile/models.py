from flask import request
from ...utilities.responseHelper import *
from ...utilities.dbHelper import DBHelper
from ...utilities.queries import *
from ...utilities.validator import vld_role, vld_edit_profile
from ...utilities.utils import split_date_time

from datetime import datetime

import time, base64

# USER MODELS ============================================================ Begin
class ProfileModels():
    # CREATE PROFILE ============================================================ Begin
    # Clear
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
            
            # Initialize Data Input ---------------------------------------- Start
            userId = datas["user_id"]
            userLevel = datas["level"]
            firstName = datas["first_name"].strip().title()
            middleName = datas["middle_name"].strip().title()
            lastName = datas["last_name"].strip().title()
            phone = datas["phone"].strip()
            # Initialize Data Input ---------------------------------------- Finish

            # Insert Data ---------------------------------------- Start
            photos = "default_avatar.png"
            timestamp = int(round(time.time()*1000))
            query = PROF_ADD_QUERY
            values = (userId, userLevel, firstName, middleName, lastName, phone, photos, timestamp, timestamp)
            DBHelper().save_data(query, values)
            # Insert Data ---------------------------------------- Finish

            # Return Response ========================================
            return success(statusCode=201)
            
        except Exception as e:
            return bad_request(str(e))
    # CREATE PROFILE ============================================================ End

    # UPDATE PROFILE ============================================================ Begin
    def edit_profile(user_id, user_role, datas):
        try:
            # Set Level Access ---------------------------------------- Start
            access = vld_role(user_role) # Access = True -> Admin
            accLevel = 1 if access else 2  # 1 = Admin | 2 = User
            # Set Level Access ---------------------------------------- Finish

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
            checkResult, result = vld_edit_profile(user_id, accLevel, fName, mName, lName, phone)
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
            # base_64 = 0
            if (photos != "") or (photos is None):
                # base_64 = base64.b64decode(photos)
                photos = result[0]["photos"]
            # Check Data ---------------------------------------- Finish
            
            # Insert Data ---------------------------------------- Start
            timestamp = int(round(time.time()*1000))
            query = PROF_UPDATE_QUERY
            values = (fName, mName, lName, phone, photos, timestamp, user_id, accLevel)
            DBHelper().save_data(query, values)
            # Insert Data ---------------------------------------- Finish

            # Log Activity Record ---------------------------------------- Start
            level = "Admin" if access else "User"
            activity = f"{level} dengan id {user_id} telah mengubah data profile."
            query = LOG_ADD_QUERY
            values = (user_id, accLevel, activity, )
            DBHelper().save_data(query, values)
            # Log Activity Record ---------------------------------------- Finish

            # Return Response ======================================== 
            return success(message="Updated!")
            
        except Exception as e:
            return bad_request(str(e))
    # UPDATE PROFILE ============================================================ End

    # GET PROFILE ============================================================ Begin
    # Clear
    def view_profile(user_id, user_role, datas):
        try:
            # Set Level Access ---------------------------------------- Start
            access = vld_role(user_role) # Access = True -> Admin
            accLevel = 1 if access else 2  # 1 = Admin | 2 = User
            # Set Level Access ---------------------------------------- Finish

            # Checking Request Body ---------------------------------------- Start
            if len(datas) != 0:            
                if "user_id" not in datas:
                    return parameter_error("Missing 'user_id' in request body.")
                
                user_id = datas["user_id"]
                accLevel = 2
                if user_id == "":
                    return defined_error("Id user tidak boleh kosong.", "Defined Error", 499)
            # Checking Request Body ---------------------------------------- Finish
            
            # Get Data From Profile ---------------------------------------- Start
            query = PROF_GET_BY_ID_QUERY
            values = (user_id, accLevel)
            result1 = DBHelper().get_data(query, values)
            if len(result1) < 1 or result1 is None:
                return not_found("Data user tidak dapat ditemukan.")
            # Get Data From Profile ---------------------------------------- Finish

            # Get Data From Account ---------------------------------------- Start
            query = ADM_GET_BY_ID_QUERY if accLevel == 1 else USR_GET_BY_ID_QUERY
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
                if accLevel == 1:
                    item["photos"] = f"{request.url_root}profile/media/admin/{item['photos']}"
                else:
                    item["photos"] = f"{request.url_root}profile/media/user/{item['photos']}"
            # Generate File URL ---------------------------------------- Finish

            # Response Data ---------------------------------------- Start
            lastSignin = split_date_time(datetime.fromtimestamp(result2[0]['last_active']/1000))
            createdAt = split_date_time(datetime.fromtimestamp(result1[0]['created_at']/1000))
            updatedAt = split_date_time(datetime.fromtimestamp(result1[0]['updated_at']/1000))
            response = {
                "id" : result1[0]["id"],
                "username" : result2[0]["username"],
                "first_name" : result1[0]["first_name"],
                "middle_name" : result1[0]["middle_name"],
                "last_name" : result1[0]["last_name"],
                "email" : result2[0]["email"],
                "status" : "Active" if result1[0]["is_delete"] == 0 else "Blocked",
                "level" : "Admin" if access else "User",
                "last_active" : lastSignin,
                "created_at" : createdAt, 
                "updated_at" : updatedAt,
                "phone" : result1[0]["phone"] if result1[0]["phone"] != "" else "08xx1234xxxx",
                "photos" : result1[0]["photos"]
            }
            # Response Data ---------------------------------------- Finish

            # Return Response ======================================== 
            return success_data(response)
            
        except Exception as e:
            return bad_request(str(e))
    # GET PROFILE ============================================================ End

    # GET DETAIL PHOTO PROFILE ============================================================ Begin
    def get_photo_profile(user_id, user_role):
        try:
            # Set Level Access ---------------------------------------- Start
            access = vld_role(user_role) # Access = True -> Admin
            accLevel = 1 if access else 2  # 1 = Admin | 2 = User
            # Set Level Access ---------------------------------------- Finish
            
            # Get Data From Profile ---------------------------------------- Start
            query = PROF_GET_BY_ID_QUERY
            values = (user_id, accLevel)
            result1 = DBHelper().get_data(query, values)
            if len(result1) < 1 or result1 is None:
                return not_found("Data user tidak dapat ditemukan.")
            # Get Data From Profile ---------------------------------------- Finish

            # Get Data From Account ---------------------------------------- Start
            query = ADM_GET_BY_ID_QUERY if accLevel == 1 else USR_GET_BY_ID_QUERY
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
    # GET DETAIL PHOTO PROFILE ============================================================ End
# USER MODELS ============================================================ End
