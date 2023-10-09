from ...utilities.responseHelper import invalid_params, parameter_error, defined_error, bad_request, success, success_data
from ...utilities.dbHelper import DBHelper
from ...utilities.queries import *
from ...utilities.validator import vld_category, vld_role

import time

# CATEGORY MODEL CLASS ============================================================ Begin
class CategoryModels():
    # CREATE CATEGORY ============================================================ Begin
    def add_category(user_id, user_role, datas):

        try:
            # Access Validation ---------------------------------------- Start
            access, message = vld_role(user_role)
            if not access:
                return defined_error(message, "Forbidden", 403)
            # Access Validation ---------------------------------------- Finish

            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            requiredData = ["category"]
            if requiredData not in datas:
                return parameter_error(f"Missing {requiredData} in Request Body")
            # Checking Request Body ---------------------------------------- Finish
            
            # Data Validation ---------------------------------------- Start
            category = datas["category"].strip()
            ctgrCheck = vld_category(category)
            if len(ctgrCheck) != 0:
                return defined_error(ctgrCheck, "Bad Request", 400)
            # Data Validation ---------------------------------------- Finish
            
            # Insert Data ---------------------------------------- Start
            timestamp = int(round(time.time()*1000))
            query = CTGR_ADD_QUERY
            values = (category, timestamp, user_id, timestamp, user_id)
            DBHelper().save_data(query, values)
            # Insert Data ---------------------------------------- Finish

            # Log Activity Record ---------------------------------------- Start
            activity = f"Admin dengan id {user_id} menambahkan kategori baru: {category}"
            query = LOG_ADD_QUERY
            values = (user_id, activity, )
            DBHelper().save_data(query, values)
            # Log Activity Record ---------------------------------------- Finish

            # Return Response ======================================== 
            return success("Successed!")
        
        except Exception as e:
            return bad_request(str(e))
    # CREATE CATEGORY ============================================================ End

    # GET DETAIL CATEGORY ============================================================ Begin
    def view_category(user_role, datas):
        try:
            # Access Validation ---------------------------------------- Start
            access, message = vld_role(user_role)
            if not access:
                return defined_error(message, "Forbidden", 403)
            # Access Validation ---------------------------------------- Finish

            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            requiredData = ["category_id"]
            if requiredData not in datas:
                return parameter_error(f"Missing {requiredData} in Request Body")
            # Checking Request Body ---------------------------------------- Finish
            
            ctgrId = datas["category_id"].strip()
            
            # Checking Data ---------------------------------------- Start
            query = CTGR_GET_BY_ID_QUERY
            values = (ctgrId,)
            result = DBHelper.get_data(query, values)
            if len(result) == 0 :
                return defined_error("Kategori tidak dapat ditemukan.")
            # Checking Data ---------------------------------------- Finish
            
            # Response Data ---------------------------------------- Start
            response = {
                "category_id" : result[0]["id"],
                "category" : result[0]["category"],
                "created_at": result[0]["created_at"]
            }
            # Response Data ---------------------------------------- Finish

            # Return Response ======================================== 
            return success_data("Successed!", response)
        
        except Exception as e:
            return bad_request(str(e))
    # GET DETAIL CATEGORY ============================================================ End

    # UPDATE CATEGORY ============================================================ Begin
    def edit_category(user_id, user_role,  datas):
        try:
            # Access Validation ---------------------------------------- Start
            access, message = vld_role(user_role)
            if not access:
                return defined_error(message, "Forbidden", 403)
            # Access Validation ---------------------------------------- Finish

            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            requiredData = ["category_id", "category"]
            for req in requiredData:
                if req not in datas:
                    return parameter_error(f"Missing {req} in Request Body")
            # Checking Request Body ---------------------------------------- Finish
            
            ctgrId = datas["category_id"].strip()
            ctgr = datas["category"].strip()
            
            # Data Validation ---------------------------------------- Start
            query = CTGR_GET_BY_ID_QUERY
            values = (ctgrId,)
            result = DBHelper.get_data(query, values)
            if len(result) == 0 :
                return defined_error("Kategori tidak dapat ditemukan.")
            
            ctgrCheck, result = vld_category(ctgr)
            if len(ctgrCheck) != 0:
                return defined_error(ctgrCheck, "Bad Request", 400)
            # Data Validation ---------------------------------------- Finish
            
            # Update Data ---------------------------------------- Start
            timestamp = int(round(time.time()*1000))
            query = CTGR_UPDATE_QUERY
            values = (ctgr, timestamp, user_id, ctgrId)
            DBHelper().save_data(query, values)
            # Update Data ---------------------------------------- Finish

            # Log Activity Record ---------------------------------------- Start
            activity = f"Admin dengan id {user_id} mengubah kategori {result[0]['category']} menjadi {ctgr}"
            query = LOG_ADD_QUERY
            values = (user_id, activity, )
            DBHelper().save_data(query, values)
            # Log Activity Record ---------------------------------------- Finish

            # Return Response ======================================== 
            return success("Successed!")
            
        except Exception as e:
            return bad_request(str(e))
    # UPDATE CATEGORY ============================================================ End

    # DELETE CATEGORY ============================================================ Begin
    def delete_category(user_id, user_role, datas):
        
        try:
            # Access Validation ---------------------------------------- Start
            access, message = vld_role(user_role)
            if not access:
                return defined_error(message, "Forbidden", 403)
            # Access Validation ---------------------------------------- Finish

            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            requiredData = ["category_id"]
            if requiredData not in datas:
                return parameter_error(f"Missing {requiredData} in Request Body")
            # Checking Request Body ---------------------------------------- Finish
            
            ctgrId = datas["category_id"].strip()
            
            # Data Validation ---------------------------------------- Start
            query = CTGR_GET_BY_ID_QUERY
            values = (ctgrId,)
            result = DBHelper().get_data(query, values)
            if len(result) == 0 :
                return defined_error("Kategori tidak dapat ditemukan.", "Bad Request", 400)
            # Data Validation ---------------------------------------- Finish
            
            # Delete Data ---------------------------------------- Start
            timestamp = int(round(time.time()*1000))
            query = CTGR_DELETE_QUERY
            values = (timestamp, user_id, ctgrId)
            DBHelper().save_data(query, values)
            # Delete Data ---------------------------------------- Finish

            # Log Activity Record ---------------------------------------- Start
            activity = f"Admin dengan id {user_id} menghapus kategori {ctgrId}"
            query = LOG_ADD_QUERY
            values = (user_id, activity, )
            DBHelper().save_data(query, values)
            # Log Activity Record ---------------------------------------- Finish

            # Return Response ======================================== 
            return success("Successed!")
            
        except Exception as e:
            return bad_request(str(e))
    # DELETE CATEGORY ============================================================ End

    # GET ALL CATEGORY ============================================================ Begin
    def view_all_category():
        try:
            # Checking Data ---------------------------------------- Start
            query = CTGR_GET_QUERY
            result = DBHelper().execute(query)
            if len(result) == 0 or result == None:
                return defined_error("Belum ada kategori.", "Bad Request", 400)
            # Checking Data ---------------------------------------- Finish
            
            # Response Data ---------------------------------------- Start
            response = []
            for rsl in result:
                data = {
                    "category_id" : rsl["id"],
                    "category" : rsl["category"],
                    "created_at": rsl["created_at"]
                }
                response.append(data)
            # Response Data ---------------------------------------- Finish
            
            # Return Response ======================================== 
            return success_data("Successed!", response)
        
        except Exception as e:
            return bad_request(str(e))
    # GET ALL CATEGORY ============================================================ End
# CATEGORY MODEL CLASS ============================================================ End