from ...utilities.responseHelper import *
from ...utilities.dbHelper import DBHelper
from ...utilities.queries import *
from ...utilities.validator import vld_greeting, vld_role
from ...utilities.utils import *

from datetime import datetime
import time

# GREETING MODEL CLASS ============================================================ Begin
class GreetingModels():
    # CREATE GREETING ============================================================ Begin
    # Clear
    def add_greeting(datas):   
        try:
            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            requiredData = ["invitation_code", "name", "status", "greeting"]
            for req in requiredData:
                if req not in datas:
                    return parameter_error(f"Missing {req} in Request Body")
            # Checking Request Body ---------------------------------------- Finish
            
            # Intialize ---------------------------------------- Start
            invCode = datas["invitation_code"]
            name = datas["name"]
            status = datas["status"]
            greeting = datas["greeting"]
            # Intialize ---------------------------------------- Finish

            # Data Validation ---------------------------------------- Start
            checkResult = vld_greeting(invCode,name,status,greeting)
            if len(checkResult) > 0:
                return defined_error(checkResult, "Bad Request", 400)
            # Data Validation ---------------------------------------- Finish

            # Get User ID ---------------------------------------- Start
            query = INV_CHK_CODE_QUERY
            values = (invCode,)
            result = DBHelper().get_data(query, values)
            if len(result) < 0:
                return not_found("Data undangan tidak dapat ditemukan.")
            owner_id = result[0]["user_id"]
            # Get User ID ---------------------------------------- End
            
            # Insert Data ---------------------------------------- Start
            timestamp = int(round(time.time()*1000))
            query = GRTG_ADD_QUERY
            values = (name, status, greeting, invCode, owner_id, timestamp, )
            DBHelper().save_data(query, values)
            # Insert Data ---------------------------------------- Finish

            # Return Response ======================================== 
            return success(statusCode=201)
        
        except Exception as e:
            return bad_request(str(e))
    # CREATE GREETING ============================================================ End

    # GET ALL GREETING ============================================================ Begin
    # Clear
    def view_greeting(user_id, user_role, datas):
        try:
            # Access Validation ======================================== 
            access = vld_role(user_role)

            # Checking Request Body ---------------------------------------- Start
            if access: # Access = True -> Admin
                if "user_id" not in datas:
                    return parameter_error("Missing 'user_id' in request body.")
                
                user_id = datas["user_id"]
                if user_id == "":
                    return defined_error("Id user tidak boleh kosong.", "Defined Error", 499)
            # Checking Request Body ---------------------------------------- Finish

            # Checking Data ---------------------------------------- Start
            query = GRTG_GET_GROUP_COUNT_QUERY
            values = (user_id, )
            result = DBHelper().get_data(query, values)
            if len(result) < 1:
                return not_found(f"Data ucapan selamat untuk user {user_id} tidak dapat ditemukan.")
            # Checking Data ---------------------------------------- Finish

            # Get Join Data ---------------------------------------- Start
            query = CTGR_GET_ALL_QUERY
            category = DBHelper().execute(query)
            query = INV_CHK_CODE_QUERY
            # Get Join Data ---------------------------------------- Finish

            # Set Join Data ---------------------------------------- Start
            for rsl in result:
                values = (rsl['invitation_code'], )
                invitation = DBHelper().get_data(query, values)
                for inv in invitation:
                    if rsl['invitation_code'] == inv['code']:
                        rsl['category_id'] = inv['category_id']
            
            for rsl in result:
                for ctg in category:
                    if rsl['category_id'] == ctg['id']:
                        rsl['category'] = ctg['category']
            # Set Join Data ---------------------------------------- Finish
            
            # Response Data ---------------------------------------- Start
            response = []
            for rsl in result:
                data = {
                    "greeting_id" : rsl["id"],
                    "category_id" : rsl["category_id"],
                    "category" : rsl["category"],
                    "user_owner" : rsl["user_id"],
                    "invitation_code" : rsl["invitation_code"],
                    "absent" : rsl["absent"],
                    "present" : rsl["present"],
                    "count" : rsl["count"]
                }
                response.append(data)
            # Response Data ---------------------------------------- Finish
            
            # Return Response ======================================== 
            return success_data(response)
        
        except Exception as e:
            return bad_request(str(e))
    # GET ALL GREETING ============================================================ End

    # # GET ALL GREETING ============================================================ Begin
    # def view_greeting_by_user(user_id, user_role):
    #     try:
    #         # Access Validation ---------------------------------------- Start
    #         access, message = vld_role(user_role)
    #         if access: # True = Admin
    #             return defined_error("Hanya User yang dapat mengakses Menu ini.", "Forbidden", 403)
    #         # Access Validation ---------------------------------------- Finish

    #         # Checking Data ---------------------------------------- Start
    #         query = GRTG_GET_BY_USER_QUERY
    #         values = (user_id,)
    #         result = DBHelper().get_data(query,values)
    #         if len(result) == 0 or result == None:
    #             return defined_error("Belum ada ucapan selamat dari calon tamu.", "Bad Request", 400)
    #         # Checking Data ---------------------------------------- Finish
            
    #         # Response Data ---------------------------------------- Start
    #         response = []
    #         for rsl in result:
    #             data = {
    #                 "greeting_id" : rsl["id"],
    #                 "name" : rsl["name"],
    #                 "email" : rsl["email"],
    #                 "greeting" : rsl["greeting"],
    #                 "invitation_code" : rsl["invitation_code"],
    #                 "user_owner" : rsl["user_id"],
    #                 "created_at": rsl["created_at"]
    #             }
    #             response.append(data)
    #         # Response Data ---------------------------------------- Finish
            
    #         # Return Response ======================================== 
    #         return success_data("Successed!", response)
        
    #     except Exception as e:
    #         return bad_request(str(e))
    # # GET ALL GREETING ============================================================ End

    # GET DETAIL GREETING ============================================================ Begin
    def view_detail_greeting(user_id, user_role, datas):
        try:
            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            invCode = datas["invitation_code"]
            if user_id == "":
                return defined_error("Kode undangan tidak boleh kosong.", "Defined Error", 499)
            # Checking Request Body ---------------------------------------- Finish
            
            # Checking Data ---------------------------------------- Start
            query = GRTG_GET_BY_CODE_QUERY
            values = (invCode,)
            result = DBHelper().get_data(query, values)
            if len(result) < 1 :
                return defined_error("Ucapan selamat tidak dapat ditemukan.")
            # Checking Data ---------------------------------------- Finish
            
            # Response Data ---------------------------------------- Start
            response = []
            for rsl in result:
                createdAt = split_date_time(datetime.fromtimestamp(rsl['created_at']/1000))
                data = {
                    "greeting_id" : rsl["id"],
                    "name" : rsl["name"],
                    "status" : "Hadir" if rsl["status"] == 1 else "Tidak Hadir",
                    "message" : rsl["message"],
                    "invitation_code" : rsl["invitation_code"],
                    "user_owner" : rsl["user_id"],
                    "created_at": createdAt
                }
                response.append(data)
            # Response Data ---------------------------------------- Finish

            # Return Response ======================================== 
            return success_data(response)
        
        except Exception as e:
            return bad_request(str(e))
    # GET DETAIL GREETING ============================================================ End

    # # UPDATE GREETING ============================================================ Begin
    # def edit_category(user_id, user_role,  datas):
    #     try:
    #         # Access Validation ---------------------------------------- Start
    #         access, message = vld_role(user_role)
    #         if not access:
    #             return defined_error(message, "Forbidden", 403)
    #         # Access Validation ---------------------------------------- Finish

    #         # Checking Request Body ---------------------------------------- Start
    #         if datas == None:
    #             return invalid_params()
            
    #         requiredData = ["category_id", "category"]
    #         for req in requiredData:
    #             if req not in datas:
    #                 return parameter_error(f"Missing {req} in Request Body")
    #         # Checking Request Body ---------------------------------------- Finish
            
    #         ctgrId = datas["category_id"].strip()
    #         ctgr = datas["category"].strip()
            
    #         # Data Validation ---------------------------------------- Start
    #         query = CTGR_GET_BY_ID_QUERY
    #         values = (ctgrId,)
    #         result = DBHelper.get_data(query, values)
    #         if len(result) == 0 :
    #             return defined_error("Kategori tidak dapat ditemukan.")
            
    #         ctgrCheck, result = vld_category(ctgr)
    #         if len(ctgrCheck) != 0:
    #             return defined_error(ctgrCheck, "Bad Request", 400)
    #         # Data Validation ---------------------------------------- Finish
            
    #         # Update Data ---------------------------------------- Start
    #         timestamp = int(round(time.time()*1000))
    #         query = CTGR_UPDATE_QUERY
    #         values = (ctgr, timestamp, timestamp, ctgrId)
    #         DBHelper().save_data(query, values)
    #         # Update Data ---------------------------------------- Finish

    #         # Log Activity Record ---------------------------------------- Start
    #         activity = f"Admin dengan id {user_id} mengubah kategori {result[0]['category']} menjadi {ctgr}"
    #         query = LOG_ADD_QUERY
    #         values = (user_id, activity, )
    #         DBHelper().save_data(query, values)
    #         # Log Activity Record ---------------------------------------- Finish

    #         # Return Response ======================================== 
    #         return success("Successed!")
            
    #     except Exception as e:
    #         return bad_request(str(e))
    # # UPDATE GREETING ============================================================ End

    # DELETE GREETING ============================================================ Begin
    def delete_greeting(user_id, user_role, datas):     
        try:
            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            requiredData = ["greeting_id"]
            if requiredData not in datas:
                return parameter_error(f"Missing {requiredData} in Request Body")
            # Checking Request Body ---------------------------------------- Finish
            
            grtgId = datas["greeting_id"].strip()
            
            # Data Validation ---------------------------------------- Start
            query = GRTG_GET_BY_ID_QUERY
            values = (grtgId,)
            result = DBHelper().get_data(query, values)
            if len(result) == 0 :
                return defined_error("Ucapan selamat tidak dapat ditemukan.", "Bad Request", 400)
            # Data Validation ---------------------------------------- Finish
            
            # Delete Data ---------------------------------------- Start
            timestamp = int(round(time.time()*1000))
            query = GRTG_DELETE_QUERY
            values = (timestamp, user_id, grtgId)
            DBHelper().save_data(query, values)
            # Delete Data ---------------------------------------- Finish

            # Log Activity Record ---------------------------------------- Start
            activity = f"Ucapan selamat dari: {result[0]['email']}, telah dihapus oleh {user_role} dengan id {user_id}"
            query = LOG_ADD_QUERY
            values = (user_id, activity, )
            DBHelper().save_data(query, values)
            # Log Activity Record ---------------------------------------- Finish

            # Return Response ======================================== 
            return success("Successed!")
            
        except Exception as e:
            return bad_request(str(e))
    # DELETE GREETING ============================================================ End
    
    # GET ROW-COUNT GREETING ============================================================ Begin
    def get_count_greeting(user_id):
        try:
            # Get Data By User Id ---------------------------------------- Start
            query = GRTG_GET_BY_USER_QUERY
            values = (user_id, )
            result = DBHelper().get_count_filter_data(query, values)
            # Get Data By User Id ---------------------------------------- Finish
            print(result)

            # Checking Data ---------------------------------------- Start
            if result == 0 or result == None :
                return defined_error("Number of greetings not found.")
            # Checking Data ---------------------------------------- Finish
            
            # Response Data ---------------------------------------- Start
            response = {
                "greeting_count" : result
            }
            # Response Data ---------------------------------------- Finish

            # Return Response ======================================== 
            return success_data(response)
        
        except Exception as e:
            return bad_request(str(e))
    # GET ROW-COUNT GREETING ============================================================ End
# GREETING MODEL CLASS ============================================================ End