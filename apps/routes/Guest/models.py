from ...utilities.responseHelper import *
from ...utilities.dbHelper import DBHelper
from ...utilities.queries import *
from ...utilities.validator import vld_guest, vld_role
from ...utilities.utils import split_date_time

from datetime import datetime
import time

# GUEST MODEL CLASS ============================================================ Begin
class GuestModels():
    # CREATE GUEST ============================================================ Begin
    def add_guest(user_id, user_role, datas):   
        try:
            # Set Access Level ---------------------------------------- Start
            access = vld_role(user_role)
            accLevel = 2
            if access: # Access = True -> Admin
                return authorization_error()
            # Set Access Level ---------------------------------------- Finish
            
            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            requiredData = ["invitation_code", "name", "address", "phone"]
            for req in requiredData:
                if req not in datas:
                    return parameter_error(f"Missing {req} in Request Body")
            # Checking Request Body ---------------------------------------- Finish
            
            # Intialize ---------------------------------------- Start
            invCode = datas["invitation_code"]
            name = datas["name"]
            address = datas["address"]
            phone = datas["phone"]
            # Intialize ---------------------------------------- Finish

            # Data Validation ---------------------------------------- Start
            checkResult, phone = vld_guest(name, address, phone, invCode)
            if len(checkResult) != 0:
                return defined_error(checkResult, "Bad Request", 400)
            # Data Validation ---------------------------------------- Finish

            # Get User ID ---------------------------------------- Start
            query = INV_CHK_CODE_QUERY
            values = (invCode,)
            result = DBHelper().get_data(query, values)
            if len(result) < 1:
                return not_found(f"Data undangan dengan kode {invCode} tidak dapat ditemukan.")
            # Get User ID ---------------------------------------- End
            
            # Insert Data ---------------------------------------- Start
            inv = result[0]
            timestamp = int(round(time.time()*1000))
            query = GUEST_ADD_QUERY
            values = (user_id, accLevel, inv['category_id'], invCode, name, address, phone, timestamp, user_id, timestamp, user_id)
            DBHelper().save_data(query, values)
            # Insert Data ---------------------------------------- Finish

            # Log Activity Record ---------------------------------------- Start
            activity = f"User dengan id {user_id} menambahkan data tamu baru: {name}."
            query = LOG_ADD_QUERY
            values = (user_id, accLevel, activity, timestamp, )
            DBHelper().save_data(query, values)
            # Log Activity Record ---------------------------------------- Finish

            # Return Response ======================================== 
            return success(statusCode=201)
        
        except Exception as e:
            return bad_request(str(e))
    # CREATE GUEST ============================================================ End

    # GET ALL GUEST ============================================================ Begin
    # Clear
    def view_guest(user_id, user_role, datas):
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
            query = GUEST_GET_GROUP_COUNT_QUERY
            values = (user_id, )
            result = DBHelper().get_data(query, values)
            if len(result) < 1 or result is None:
                return not_found(f"Data tamu untuk user {user_id} tidak dapat ditemukan.")
            # Checking Data ---------------------------------------- Finish

            # Get Join Data ---------------------------------------- Start
            query = CTGR_GET_ALL_QUERY
            category = DBHelper().execute(query)
            query = INV_CHK_CODE_QUERY
            # Get Join Data ---------------------------------------- Finish

            # Set Join Data ---------------------------------------- Start
            print(result)
            for rsl in result:
                values = (rsl['invitation_code'], )
                invitation = DBHelper().get_data(query, values)
                for inv in invitation:
                    if rsl['invitation_code'] == inv['code']:
                        rsl['invitation_id'] = inv['id']
                for ctg in category:
                    if rsl['category_id'] == ctg['id']:
                        rsl['category'] = ctg['category']
            # Set Join Data ---------------------------------------- Finish

            # Response Data ---------------------------------------- Start
            response = []
            for rsl in result:
                data = {
                    "guest_id" : rsl["id"],
                    "category_id" : rsl['category_id'],
                    "invitation_id" : rsl['invitation_id'],
                    "event" : rsl['category'],
                    "invitation_code" : rsl["invitation_code"],
                    "user_owner" : rsl["user_id"],
                    "count" : rsl['count']
                }
                response.append(data)
            # Response Data ---------------------------------------- Finish
            
            # Return Response ======================================== 
            return success_data(response)
        
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

    # GET DETAIL GUEST ============================================================ Begin
    # Clear
    def view_detail_guest(user_role, datas):
        try:
            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            if "invitation_code" not in datas:
                return parameter_error("Missing 'invitation_code' in Request Body.")
            
            invCode = datas["invitation_code"]
            if invCode == "":
                return defined_error("Kode undangan tidak boleh kosong.", "Defined Error", 400)
            # Checking Request Body ---------------------------------------- Finish
            
            # Checking Data ---------------------------------------- Start
            query = GUEST_GET_BY_CODE_QUERY
            values = (invCode,)
            result = DBHelper().get_data(query, values)
            if len(result) < 1 :
                return not_found(f"Data tamu untuk kode undangan {invCode} tidak dapat ditemukan.")
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
                        rsl['invitation_id'] = inv['id']
                for ctg in category:
                    if rsl['category_id'] == ctg['id']:
                        rsl['category'] = ctg['category']
            # Set Join Data ---------------------------------------- Finish

            # Response Data ---------------------------------------- Start
            response = []
            for rsl in result:
                createdAt = split_date_time(datetime.fromtimestamp(rsl["created_at"]/1000))
                updatedAt = split_date_time(datetime.fromtimestamp(rsl["updated_at"]/1000))
                data = {
                    "guest_id" : rsl["id"],
                    "category_id" : rsl["category_id"],
                    "invitation_id" : rsl["invitation_id"],
                    "event" : rsl["category"],
                    "name" : rsl["name"],
                    "phone" : rsl["phone"],
                    "address" : rsl["address"],
                    "invitation_code" : rsl["invitation_code"],
                    "user_owner" : rsl["user_id"],
                    "created_at": createdAt,
                    "updated_at": updatedAt
                }
                response.append(data)
            # Response Data ---------------------------------------- Finish

            # Return Response ======================================== 
            return success_data(response)
        
        except Exception as e:
            return bad_request(str(e))
    # GET DETAIL GUEST ============================================================ End

    # GET DETAIL GUEST ============================================================ Begin
    # Clear
    def view_guest_by_id(datas):
        try:
            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            if "guest_id" not in datas:
                return parameter_error("Missing 'guest_id' in Request Body.")
            
            guestId = datas["guest_id"]
            if guestId == "":
                return defined_error("Id tamu tidak boleh kosong.", "Defined Error", 400)
            # Checking Request Body ---------------------------------------- Finish
            
            # Checking Data ---------------------------------------- Start
            query = GUEST_GET_BY_ID_QUERY
            values = (guestId,)
            result = DBHelper().get_data(query, values)
            if len(result) < 1 :
                return defined_error(f"Data tamu untuk kode undangan {guestId} tidak dapat ditemukan.")
            # Checking Data ---------------------------------------- Finish
            
            # Set Category ---------------------------------------- Start
            query = CTGR_GET_ALL_QUERY
            category = DBHelper().execute(query)
            for ctg in category:
                for rsl in result:
                    if rsl['category_id'] == ctg['id']:
                        rsl['category'] = ctg['category']
            # Set Category ---------------------------------------- Finish

            # Response Data ---------------------------------------- Start
            rsl = result[0]
            createdAt = split_date_time(datetime.fromtimestamp(rsl["created_at"]/1000))
            updatedAt = split_date_time(datetime.fromtimestamp(rsl["updated_at"]/1000))
            response = {
                "guest_id" : rsl["id"],
                "category_id" : rsl["category_id"],
                "event" : rsl["category"],
                "name" : rsl["name"],
                "phone" : rsl["phone"],
                "address" : rsl["address"],
                "invitation_code" : rsl["invitation_code"],
                "user_owner" : rsl["user_id"],
                "created_at": createdAt,
                "updated_at": updatedAt
            }
            # Response Data ---------------------------------------- Finish

            # Return Response ======================================== 
            return success_data(response)
        
        except Exception as e:
            return bad_request(str(e))
    # GET DETAIL GUEST ============================================================ End

    # UPDATE GUEST ============================================================ Begin
    # Clear
    def edit_guest(user_id, user_role, datas):
        try:
            # Access Validation ---------------------------------------- Start
            access = vld_role(user_role)
            accLevel = 2
            # Access Validation ---------------------------------------- Finish

            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            requiredData = ["guest_id", "invitation_code", "name", "address", "phone"]
            for req in requiredData:
                if req not in datas:
                    return parameter_error(f"Missing {req} in Request Body")
            # Checking Request Body ---------------------------------------- Finish
            
            # Inisialize Data Input ---------------------------------------- Start
            gueId = datas["guest_id"]
            invCode = datas["invitation_code"]
            name = datas["name"]
            address = datas["address"]
            phone = datas["phone"]
            # Inisialize Data Input ---------------------------------------- Finish
            
            # Data Validation ---------------------------------------- Start
            query = GUEST_GET_BY_ID_QUERY
            values = (gueId, )
            result = DBHelper().get_data(query, values)
            if len(result) < 1 :
                return not_found("Data tamu tidak dapat ditemukan.")
            
            guestCheck, phone = vld_guest(name, address, phone, invCode, False)
            if len(guestCheck) != 0:
                return defined_error(guestCheck, "Bad Request", 400)
            # Data Validation ---------------------------------------- Finish
            
            # Update Data ---------------------------------------- Start
            timestamp = int(round(time.time()*1000))
            query = GUEST_UPDATE_QUERY
            values = (name, address, phone, timestamp, user_id, gueId, )
            DBHelper().save_data(query, values)
            # Update Data ---------------------------------------- Finish

            # Log Activity Record ---------------------------------------- Start
            activity = f"{user_role.title()} dengan id {user_id} mengubah data tamu {result[0]['name']}."
            query = LOG_ADD_QUERY
            values = (user_id, accLevel, activity, timestamp, )
            DBHelper().save_data(query, values)
            # Log Activity Record ---------------------------------------- Finish

            # Return Response ======================================== 
            return success(message="Updated!")
            
        except Exception as e:
            return bad_request(str(e))
    # UPDATE GUEST ============================================================ End

    # DELETE GUEST ============================================================ Begin
    # Clear
    def delete_guest(user_id, user_role, datas):     
        try:
            print(datas)
            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            if "guest_id" not in datas:
                return parameter_error("Missing 'guest_id' in Request Body.")
            
            guestId = datas["guest_id"]
            if guestId == "":
                return defined_error("Id tamu tidak boleh kosong.", "Defined Error", 400)
            # Checking Request Body ---------------------------------------- Finish
            
            # Data Validation ---------------------------------------- Start
            query = GUEST_GET_BY_ID_QUERY
            values = (guestId,)
            result = DBHelper().get_data(query, values)
            if len(result) < 1 :
                return not_found("Data tamu tidak dapat ditemukan.")
            # Data Validation ---------------------------------------- Finish

            # Delete Data ---------------------------------------- Start
            timestamp = int(round(time.time()*1000))
            query = GUEST_DELETE_QUERY
            values = (timestamp, user_id, guestId)
            DBHelper().save_data(query, values)
            # Delete Data ---------------------------------------- Finish

            # Log Activity Record ---------------------------------------- Start
            activity = f"User dengan id {user_id} menghapus data tamu {result[0]['name']}."
            query = LOG_ADD_QUERY
            values = (user_id, 2, activity, timestamp, )
            DBHelper().save_data(query, values)
            # Log Activity Record ---------------------------------------- Finish

            # Return Response ======================================== 
            return success("Deleted!")
            
        except Exception as e:
            return bad_request(str(e))
    # DELETE GUEST ============================================================ End

    # GET ROW-COUNT GUEST ============================================================ Begin
    # Clear
    def get_count_guest(user_id):
        try:
            # Get Data By User Id ---------------------------------------- Start
            query = GUEST_GET_BY_USR_QUERY
            values = (user_id, )
            result = DBHelper().get_count_filter_data(query, values)
            # Get Data By User Id ---------------------------------------- Finish

            # Checking Data ---------------------------------------- Start
            if result < 1 or result == None :
                return not_found("Data tamu tidak dapat ditemukan.")
            # Checking Data ---------------------------------------- Finish
            
            # Response Data ---------------------------------------- Start
            response = {
                "guest_count" : result
            }
            # Response Data ---------------------------------------- Finish

            # Return Response ======================================== 
            return success_data(response)
        
        except Exception as e:
            return bad_request(str(e))
    # GET ROW-COUNT GUEST ============================================================ End
# GUEST MODEL CLASS ============================================================ End