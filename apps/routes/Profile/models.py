from ...utilities.responseHelper import invalid_params, parameter_error, defined_error, bad_request, success, success_data
from ...utilities.dbHelper import DBHelper
from ...utilities.queries import *
from ...utilities.validator import vld_role, vld_edit_profile

import time, base64

# USER MODELS ============================================================ Begin
class ProfileModels():
    # VIEW PROFILE ============================================================ Begin
    def view_profile(userId, userRole):
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
            base_64 = base64.b64encode(result[0]["photos"]).decode('utf-8')
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
            return success_data("Succeed!", response)
            
        except Exception as e:
            return bad_request(str(e))
    # VIEW PROFILE ============================================================ End

    # EDIT PROFILE ============================================================ Begin
    def edit_profile(userId, userRole, datas):
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
            if userLevel == 1:
                level = "Admin"
            elif userLevel == 2:
                level = "User"
            activity = f"{level} dengan id {userId} telah mengubah data profile."
            query = LOG_ADD_QUERY
            values = (userId, activity, )
            DBHelper().save_data(query, values)
            # Log Activity Record ---------------------------------------- Finish

            # Return Response ======================================== 
            return success("Succeed!")
            
        except Exception as e:
            return bad_request(str(e))
    # EDIT PROFILE ============================================================ End
# USER MODELS ============================================================ End
