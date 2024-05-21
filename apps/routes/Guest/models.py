from ...utilities.responseHelper import invalid_params, parameter_error, defined_error, bad_request, success, success_data
from ...utilities.dbHelper import DBHelper
from ...utilities.queries import *
from ...utilities.validator import vld_greeting, vld_role

import time

# GUEST MODEL CLASS ============================================================ Begin
class GuestModels():
    # # CREATE GUEST ============================================================ Begin
    # def add_guest(datas):   
    #     try:
    #         # Checking Request Body ---------------------------------------- Start
    #         if datas == None:
    #             return invalid_params()
            
    #         requiredData = ["invitationCode", "name", "email", "greeting"]
    #         for req in requiredData:
    #             if req not in datas:
    #                 return parameter_error(f"Missing {req} in Request Body")
    #         # Checking Request Body ---------------------------------------- Finish
            
    #         # Intialize ---------------------------------------- Start
    #         invCode = datas["invitationCode"].strip()
    #         name = datas["name"].strip().title()
    #         email = datas["email"].strip()
    #         greeting = datas["greeting"]
    #         # Intialize ---------------------------------------- Finish

    #         # Data Validation ---------------------------------------- Start
    #         checkResult = vld_greeting(invCode,name,email,greeting)
    #         if len(checkResult) != 0:
    #             return defined_error(checkResult, "Bad Request", 400)
    #         # Data Validation ---------------------------------------- Finish

    #         # Get User ID ---------------------------------------- Start
    #         query = INV_CODE_CHK_QUERY
    #         values = (invCode,)
    #         result = DBHelper().get_data(query, values)
    #         user_owner_id = result[0]["id"]
    #         # Get User ID ---------------------------------------- End
            
    #         # Insert Data ---------------------------------------- Start
    #         timestamp = int(round(time.time()*1000))
    #         query = GUEST_ADD_QUERY
    #         values = (name, email, greeting, invCode, user_owner_id, timestamp)
    #         DBHelper().save_data(query, values)
    #         # Insert Data ---------------------------------------- Finish

    #         # Log Activity Record ---------------------------------------- Start
    #         activity = f"User dengan id {user_owner_id} mendapatkan ucapan selamat dari: {email}"
    #         query = LOG_ADD_QUERY
    #         values = (user_owner_id, activity, )
    #         DBHelper().save_data(query, values)
    #         # Log Activity Record ---------------------------------------- Finish

    #         # Return Response ======================================== 
    #         return success("Succeed!")
        
    #     except Exception as e:
    #         return bad_request(str(e))
    # # CREATE GUEST ============================================================ End

    # GET ALL GUEST ============================================================ Begin
    def view_guest(user_id, user_role):
        try:
            # Access Validation ---------------------------------------- Start
            access, message = vld_role(user_role)
            if access: # False = User
                return defined_error(message, "Forbidden", 403)
            # Access Validation ---------------------------------------- Finish

            # Checking Data ---------------------------------------- Start
            query1 = GUEST_GET_GROUP_COUNT_QUERY
            values = (user_id, )
            result = DBHelper().get_data(query1, values)
            if len(result) == 0 or result == None:
                return defined_error("Belum ada daftar tamu untuk acara manapun.", "Not Found", 404)
            # Checking Data ---------------------------------------- Finish

            # Set Category ---------------------------------------- Start
            query2 = CTGR_GET_ALL_QUERY
            category = DBHelper().execute(query2)
            for ctg in category:
                for rsl in result:
                    if rsl['category_id'] == ctg['id']:
                        rsl['category_id'] = ctg['category']
            # Set Category ---------------------------------------- Finish
            
            # Response Data ---------------------------------------- Start
            response = []
            for rsl in result:
                data = {
                    "event" : rsl['category_id'],
                    "invitation_code" : rsl["code"],
                    "user_owner" : rsl["user_id"],
                    "count" : rsl['count']
                }
                response.append(data)
            # Response Data ---------------------------------------- Finish
            
            # Return Response ======================================== 
            return success_data("Successed!", response)
        
        except Exception as e:
            return bad_request(str(e))
    # GET ALL GUEST ============================================================ End

    # # GET ALL GUEST ============================================================ Begin
    # def view_guest_by_user(user_id, user_role):
    #     try:
    #         # Access Validation ---------------------------------------- Start
    #         access, message = vld_role(user_role)
    #         if access: # True = Admin
    #             return defined_error("Hanya User yang dapat mengakses Menu ini.", "Forbidden", 403)
    #         # Access Validation ---------------------------------------- Finish

    #         # Checking Data ---------------------------------------- Start
    #         query = GUEST_GET_WITH_FILTER_QUERY
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
    # # GET ALL GUEST ============================================================ End

    # # GET DETAIL GUEST ============================================================ Begin
    # def view_detail_guest(user_role, datas):
    #     try:
    #         # Checking Request Body ---------------------------------------- Start
    #         if datas == None:
    #             return invalid_params()
            
    #         requiredData = ["greeting_id"]
    #         if requiredData not in datas:
    #             return parameter_error(f"Missing {requiredData} in Request Body")
    #         # Checking Request Body ---------------------------------------- Finish
            
    #         grtgId = datas["greeting_id"].strip()
            
    #         # Checking Data ---------------------------------------- Start
    #         query = GRTG_GET_BY_ID_QUERY
    #         values = (grtgId,)
    #         result = DBHelper.get_data(query, values)
    #         if len(result) == 0 :
    #             return defined_error("Ucapan selamat tidak dapat ditemukan.")
    #         # Checking Data ---------------------------------------- Finish
            
    #         # Response Data ---------------------------------------- Start
    #         response = []
            # for rsl in result:
            #     data = {
            #         "guest_id" : rsl["id"],
            #         "event" : rsl["category_id"],
            #         "name" : rsl["name"],
            #         "alias" : rsl["alias"],
            #         "invitation_code" : rsl["code"],
            #         "user_owner" : rsl["user_id"],
            #         "created_at": rsl["created_at"]
            #     }
            #     response.append(data)
    #         # Response Data ---------------------------------------- Finish

    #         # Return Response ======================================== 
    #         return success_data("Successed!", response)
        
    #     except Exception as e:
    #         return bad_request(str(e))
    # # GET DETAIL GUEST ============================================================ End

    # # UPDATE GUEST ============================================================ Begin
    # def edit_guest(user_id, user_role,  datas):
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
    # # UPDATE GUEST ============================================================ End

    # # DELETE GUEST ============================================================ Begin
    # def delete_guest(user_id, user_role, datas):     
    #     try:
    #         # Checking Request Body ---------------------------------------- Start
    #         if datas == None:
    #             return invalid_params()
            
    #         requiredData = ["greeting_id"]
    #         if requiredData not in datas:
    #             return parameter_error(f"Missing {requiredData} in Request Body")
    #         # Checking Request Body ---------------------------------------- Finish
            
    #         grtgId = datas["greeting_id"].strip()
            
    #         # Data Validation ---------------------------------------- Start
    #         query = GRTG_GET_BY_ID_QUERY
    #         values = (grtgId,)
    #         result = DBHelper().get_data(query, values)
    #         if len(result) == 0 :
    #             return defined_error("Ucapan selamat tidak dapat ditemukan.", "Bad Request", 400)
    #         # Data Validation ---------------------------------------- Finish
            
    #         # Delete Data ---------------------------------------- Start
    #         timestamp = int(round(time.time()*1000))
    #         query = GRTG_DELETE_QUERY
    #         values = (timestamp, user_id, grtgId)
    #         DBHelper().save_data(query, values)
    #         # Delete Data ---------------------------------------- Finish

    #         # Log Activity Record ---------------------------------------- Start
    #         activity = f"Ucapan selamat dari: {result[0]['email']}, telah dihapus oleh {user_role} dengan id {user_id}"
    #         query = LOG_ADD_QUERY
    #         values = (user_id, activity, )
    #         DBHelper().save_data(query, values)
    #         # Log Activity Record ---------------------------------------- Finish

    #         # Return Response ======================================== 
    #         return success("Successed!")
            
    #     except Exception as e:
    #         return bad_request(str(e))
    # # DELETE GUEST ============================================================ End

    # GET ROW-COUNT GUEST ============================================================ Begin
    def get_count_guest(user_id):
        try:
            # Get Data By User Id ---------------------------------------- Start
            query = GUEST_GET_BY_USR_QUERY
            values = (user_id, )
            result = DBHelper().get_count_filter_data(query, values)
            # Get Data By User Id ---------------------------------------- Finish

            # Checking Data ---------------------------------------- Start
            if result == 0 or result == None :
                return defined_error("Number of guests not found.")
            # Checking Data ---------------------------------------- Finish
            
            # Response Data ---------------------------------------- Start
            response = {
                "guest_count" : result
            }
            # Response Data ---------------------------------------- Finish

            # Return Response ======================================== 
            return success_data("Successed!", response)
        
        except Exception as e:
            return bad_request(str(e))
    # GET ROW-COUNT GUEST ============================================================ End
# GUEST MODEL CLASS ============================================================ End