from flask_jwt_extended import create_access_token, decode_token

from ...utilities.responseHelper import invalid_params, parameter_error, defined_error, bad_request, success, success_data
from ...utilities.dbHelper import DBHelper
from ...utilities.queries import *
from ...utilities.utils import hashPassword
from ...utilities.validator import vld_user_regis, vld_signin, vld_role, vld_edit_profile

import time, base64

# USER MODELS ============================================================ Begin
class UserModels():
    # CREATE ADMIN ============================================================ Begin
    def create_user(datas):
        try:
            # Validation Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            requiredData = ["first_name", "last_name", "email", "password", "retype_password"]
            for req in requiredData:
                if req not in datas:
                    return parameter_error(f"Missing {req} in Request Body")
            # Validation Request Body ---------------------------------------- Finish
            
            # Initialize Data ---------------------------------------- Start
            firstName = datas["first_name"].strip().title()
            lastName = datas["last_name"].strip().title()
            email = datas["email"].strip().lower()
            password = datas["password"].strip()
            retypePassword = datas["retype_password"].strip()
            # Initialize Data ---------------------------------------- Finish

            # Data Validation ---------------------------------------- Start
            checkResult = vld_user_regis(firstName, lastName, email, password, retypePassword)
            if len(checkResult) != 0:
                return defined_error(checkResult, "Bad Request", statusCode=400)
            # Data Validation ---------------------------------------- Finish
            
            # Insert Data ---------------------------------------- Start
            passEncrypt = hashPassword(password)
            timestamp = int(round(time.time()*1000))
            query = USR_ADD_QUERY
            values = (firstName, email, passEncrypt, timestamp, timestamp)
            resReturn = DBHelper().save_return(query, values)
            if resReturn == None:
                return defined_error("Gagal menyimpan data.", "Bad Request", 400)
            # Insert Data ---------------------------------------- Finish

            # Insert Profile ---------------------------------------- Start
            userId = resReturn
            level = 2  # 1:Admin, 2:User
            query = PROF_ADD_QUERY
            values = (userId, level, firstName, "", lastName, "", 0, timestamp, timestamp)
            DBHelper().save_data(query, values)
            # Insert Profile ---------------------------------------- Finish

            # Log Activity Record ---------------------------------------- Start
            activity = f"User baru dengan id {userId} telah berhasil mendaftar."
            query = LOG_ADD_QUERY
            values = (userId, activity, )
            DBHelper().save_data(query, values)
            # Log Activity Record ---------------------------------------- Finish

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
    def view_profile_user(userId, userRole):
        try:
            # Set Level User ---------------------------------------- Start
            userLevel = 1  # 1 = Admin
            access, message = vld_role(userRole)
            if not access:
                userLevel = 2  # 2 = User
            # Set Level User ---------------------------------------- Finish
            
            # Get Data ---------------------------------------- Start
            query = PROF_GET_BY_ID_QUERY
            values = (userId, userLevel)
            result = DBHelper().get_data(query, values)
            if len(result) == 0 :
                return defined_error("Gagal menemukan data user.", "Bad Request", 400)
            # Get Data ---------------------------------------- Finish

            # Response Data ---------------------------------------- Start
            print(result[0]["photos"])
            base_64 = base64.b64encode(result[0]["photos"]).decode('utf-8')
            print("base64", base_64)
            response = {
                "id" : result[0]["id"],
                "first_name" : result[0]["first_name"],
                "middle_name" : result[0]["middle_name"],
                "last_name" : result[0]["last_name"],
                "phone" : result[0]["phone"],
                "photos" : base_64
            }
            # Response Data ---------------------------------------- Finish

            # Return Response ======================================== 
            return success_data("Successed!", response)
            
        except Exception as e:
            return bad_request(str(e))
    # VIEW PROFILE ============================================================ End

    # EDIT PROFILE ============================================================ Begin
    def edit_profile_user(userId, userRole, datas):
        try:
            # Set Level User ---------------------------------------- Start
            userLevel = 1  # 1 = Admin
            access, message = vld_role(userRole)
            if not access:
                userLevel = 2  # 2 = User
            # Set Level User ---------------------------------------- Finish

            # Validation Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            requiredData = ["first_name", "middle_name", "last_name", "phone", "photos"]
            for req in requiredData:
                if req not in datas:
                    return parameter_error(f"Missing {req} in Request Body")
            # Validation Request Body ---------------------------------------- Finish
            
            # Initialize Data ---------------------------------------- Start
            fName = datas["first_name"].strip().title()
            mName = datas["middle_name"].strip()
            lName = datas["last_name"].strip()
            phone = datas["phone"].strip()
            photos = datas["photos"]
            # Initialize Data ---------------------------------------- Finish

            # Data Validation ---------------------------------------- Start
            checkResult, result = vld_edit_profile(userId, userLevel, fName, mName, lName, phone)
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
            values = (fName, mName, lName, phone, base_64, timestamp, userId, userLevel)
            DBHelper().save_data(query, values)
            # Insert Data ---------------------------------------- Finish

            # Log Activity Record ---------------------------------------- Start
            activity = f"User dengan id {userId} telah mengubah data profile."
            query = LOG_ADD_QUERY
            values = (userId, activity, )
            DBHelper().save_data(query, values)
            # Log Activity Record ---------------------------------------- Finish

            # Return Response ======================================== 
            return success("Successed!")
            
        except Exception as e:
            return bad_request(str(e))
    # EDIT PROFILE ============================================================ End
# USER MODELS ============================================================ End
