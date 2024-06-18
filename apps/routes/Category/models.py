from ...utilities.responseHelper import *
from ...utilities.dbHelper import DBHelper
from ...utilities.queries import *
from ...utilities.validator import vld_role, vld_category
from ...utilities.utils import split_date_time
from datetime import datetime

import time, json

# CATEGORY MODEL CLASS ============================================================ Begin
class CategoryModels():
    # CREATE CATEGORY ============================================================ Begin
    # Clear
    def add_category(user_id, user_role, datas):
        try:
            # Access Validation ---------------------------------------- Start
            access = vld_role(user_role)
            if not access: # Access = True -> Admin
                return authorization_error()
            # Access Validation ---------------------------------------- Finish

            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            requiredData = ["category", "format_data"]
            for req in requiredData:
                if req not in datas:
                    return parameter_error(f"Missing {req} in Request Body.")
            # Checking Request Body ---------------------------------------- Finish
            
            # Data Validation ---------------------------------------- Start
            category = datas["category"].strip()
            formatData = datas["format_data"]
            ctgrCheck = vld_category(category, formatData)
            if len(ctgrCheck) != 0:
                return defined_error(ctgrCheck, "Bad Request", 400)
            # Data Validation ---------------------------------------- Finish
            
            # Insert Data ---------------------------------------- Start
            timestamp = int(round(time.time()*1000))
            formatData = json.dumps(formatData)
            query = CTGR_ADD_QUERY
            values = (category, formatData, timestamp, user_id, timestamp, user_id)
            DBHelper().save_data(query, values)
            # Insert Data ---------------------------------------- Finish

            # Log Activity Record ---------------------------------------- Start
            activity = f"Admin dengan id {user_id} menambahkan kategori baru: {category}."
            query = LOG_ADD_QUERY
            values = (user_id, 1, activity, timestamp, )
            DBHelper().save_data(query, values)
            # Log Activity Record ---------------------------------------- Finish

            # Return Response ======================================== 
            return success(statusCode=201)
        
        except Exception as e:
            return bad_request(str(e))
    # CREATE CATEGORY ============================================================ End

    # GET ALL CATEGORY ============================================================ Begin
    # Clear
    def view_category():
        try:
            # Checking Data ---------------------------------------- Start
            query = CTGR_GET_ALL_QUERY
            result = DBHelper().execute(query)
            if len(result) < 1 or result is None:
                return not_found("Data kategori tidak dapat ditemukan.")
            # Checking Data ---------------------------------------- Finish
            
            # Response Data ---------------------------------------- Start
            response = []
            for rsl in result:
                createdAt = split_date_time(datetime.fromtimestamp(rsl['created_at']/1000))
                data = {
                    "category_id" : rsl["id"],
                    "category" : rsl["category"],
                    "format_data" : json.loads(rsl["format_data"]),
                    "created_at": createdAt
                }
                response.append(data)
            # Response Data ---------------------------------------- Finish
            
            # Return Response ======================================== 
            return success_data(response)
        
        except Exception as e:
            return bad_request(str(e))
    # GET ALL CATEGORY ============================================================ End

    # UPDATE CATEGORY ============================================================ Begin
    # Clear
    def edit_category(user_id, user_role, datas):
        try:
            # Access Validation ---------------------------------------- Start
            access = vld_role(user_role)
            if not access: # Access = True -> Admin
                return authorization_error()
            # Access Validation ---------------------------------------- Finish

            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            requiredData = ["category_id", "category", "format_data"]
            for req in requiredData:
                if req not in datas:
                    return parameter_error(f"Missing {req} in Request Body.")
            # Checking Request Body ---------------------------------------- Finish
            
            # Initialize Data Input ---------------------------------------- Start
            catgId = datas["category_id"]
            category = datas["category"].strip()
            formatData = datas["format_data"]
            # Initialize Data Input ---------------------------------------- Finish
            
            # Data Validation ---------------------------------------- Start
            query = CTGR_GET_BY_ID_QUERY
            values = (catgId,)
            result = DBHelper().get_data(query, values)
            if len(result) < 1 :
                return not_found(f"Data kategori dengan id {catgId} tidak dapat ditemukan.")
            
            ctgrCheck = vld_category(category, formatData, False)
            if len(ctgrCheck) != 0:
                return defined_error(ctgrCheck, "Bad Request", 400)
            # Data Validation ---------------------------------------- Finish
            
            # Update Data ---------------------------------------- Start
            formatData = json.dumps(formatData)
            timestamp = int(round(time.time()*1000))
            query = CTGR_UPDATE_QUERY
            values = (category, formatData, timestamp, user_id, catgId)
            DBHelper().save_data(query, values)
            # Update Data ---------------------------------------- Finish

            # Log Activity Record ---------------------------------------- Start
            activity = f"Admin dengan id {user_id} mengubah kategori {result[0]['category']} menjadi {category}."
            query = LOG_ADD_QUERY
            values = (user_id, 1, activity, timestamp, )
            DBHelper().save_data(query, values)
            # Log Activity Record ---------------------------------------- Finish
            print("oke")

            # Return Response ======================================== 
            return success(message="Updated!")
            
        except Exception as e:
            return bad_request(str(e))
    # UPDATE CATEGORY ============================================================ End

    # DELETE CATEGORY ============================================================ Begin
    # Clear
    def delete_category(user_id, user_role, datas):
        try:
            # Access Validation ---------------------------------------- Start
            access = vld_role(user_role)
            if not access: # Access = True -> Admin
                return authorization_error()
            # Access Validation ---------------------------------------- Finish

            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            if "category_id" not in datas:
                return parameter_error("Missing 'category_id' in Request Body.")
            
            catgId = datas["category_id"]
            if catgId == "":
                return defined_error("Id kategori tidak boleh kosong.", "Defined Error", 499)
            # Checking Request Body ---------------------------------------- Finish
            
            # Checking Data ---------------------------------------- Finish
            query = CTGR_GET_BY_ID_QUERY
            values = (catgId,)
            result = DBHelper().get_count_filter_data(query, values)
            if result < 1 or result is None:
                return not_found(f"Kategori dengan Id {catgId} tidak dapat ditemukan.")
            # Checking Data ---------------------------------------- Finish
            
            # Delete Data ---------------------------------------- Start
            timestamp = int(round(time.time()*1000))
            query = CTGR_DELETE_QUERY
            values = (timestamp, user_id, catgId)
            DBHelper().save_data(query, values)
            # Delete Data ---------------------------------------- Finish

            # Log Activity Record ---------------------------------------- Start
            activity = f"Admin dengan id {user_id} menghapus kategori {catgId}."
            query = LOG_ADD_QUERY
            values = (user_id, 1, activity, timestamp, )
            DBHelper().save_data(query, values)
            # Log Activity Record ---------------------------------------- Finish

            # Return Response ======================================== 
            return success(message="Deleted!")
            
        except Exception as e:
            return bad_request(str(e))
    # DELETE CATEGORY ============================================================ End

    # GET DETAIL CATEGORY ============================================================ Begin
    # Clear
    def view_detail_category(user_role, datas):
        try:
            # Access Validation ---------------------------------------- Start
            access = vld_role(user_role)
            if not access: # Access = True -> Admin
                return authorization_error()
            # Access Validation ---------------------------------------- Finish

            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            if "category_id" not in datas:
                return parameter_error("Missing 'category_id' in Request Body.")
            
            catgId = datas["category_id"]
            if catgId == "":
                return defined_error("Id kategori tidak boleh kosong.", "Defined Error", 400)
            # Checking Request Body ---------------------------------------- Finish
            
            # Checking Data ---------------------------------------- Start
            query = CTGR_GET_BY_ID_QUERY
            values = (catgId,)
            result = DBHelper().get_data(query, values)
            if len(result) < 1 :
                return not_found(f"Data kategori dengan Id {catgId} tidak dapat ditemukan.")
            # Checking Data ---------------------------------------- Finish
            
            # Response Data ---------------------------------------- Start
            response = {
                "category_id" : result[0]["id"],
                "category" : result[0]["category"],
                "format_data" : json.loads(result[0]["format_data"]),
                "created_at": result[0]["created_at"]
            }
            # Response Data ---------------------------------------- Finish

            # Return Response ======================================== 
            return success_data(response)
        
        except Exception as e:
            return bad_request(str(e))
    # GET DETAIL CATEGORY ============================================================ End

    # GET ROW-COUNT CATEGORY ============================================================ Begin
    # Clear
    def get_count_category():
        try:
            # Checking Data ---------------------------------------- Start
            query = CTGR_GET_ALL_QUERY
            result = DBHelper().get_count_data(query)
            if result < 1 or result is None :
                return not_found("Data kategori tidak dapat ditemukan.")
            # Checking Data ---------------------------------------- Finish
            
            # Response Data ---------------------------------------- Start
            response = {
                "category_count" : result
            }
            # Response Data ---------------------------------------- Finish

            # Return Response ======================================== 
            return success_data(response)
        
        except Exception as e:
            return bad_request(str(e))
    # GET ROW-COUNT CATEGORY ============================================================ End
# CATEGORY MODEL CLASS ============================================================ End