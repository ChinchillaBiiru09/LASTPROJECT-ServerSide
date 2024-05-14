from ...utilities.responseHelper import invalid_params, parameter_error, defined_error, bad_request, success, success_data
from ...utilities.dbHelper import DBHelper
from ...utilities.queries import *
from ...utilities.validator import vld_role, vld_invitation
from ...utilities.utils import random_number, saving_image, random_string_number

from flask import request, current_app as app
from werkzeug.utils import secure_filename

import time, os


# INVITATION MODEL CLASS ============================================================ Begin
class InvitationModels():
    # CREATE INVITATION ============================================================ Begin
    def add_invitation(userId, userRole, datas):
        try:
            # Set Level User ---------------------------------------- Start
            userLevel = 1  # 1 = Admin
            access, message = vld_role(userRole)
            if not access:
                userLevel = 2  # 2 = User
            # Set Level User ---------------------------------------- Finish

            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            requiredData = ["category_id", "template_id", "title", "wallpaper", "personal_data", "inv_setting"]
            for req in requiredData:
                if req not in datas:
                    return parameter_error(f"Missing {req} in Request Body")
            # Checking Request Body ---------------------------------------- Finish

            # Initialize Request Data ---------------------------------------- Start
            categoryId = datas["category_id"].strip()
            templateId = datas["template_id"].strip()
            title = datas["title"].title().strip()
            wallpaper = datas["wallpaper"]
            personalData = datas["personal_data"]
            invSett = datas["inv_setting"]
            # Initialize Request Data ---------------------------------------- Finish
            
            # Data Validation ---------------------------------------- Start
            randomNumber = str(random_number(5))
            invCheck, personalData = vld_invitation(categoryId, templateId, title, personalData, randomNumber)
            if len(invCheck) != 0:
                return defined_error(invCheck, "Bad Request", 400)
            # Data Validation ---------------------------------------- Finish
            
            # Saving File ---------------------------------------- Start
            # wallpaper
            wallpaperPath = ""
            if wallpaper != "":
                wallpaperFileName = secure_filename(time.strftime("%Y-%m-%d %H:%M:%S")+"_"+randomNumber+"_wallpaper.jpg")
                wallpaperPath = os.path.join(app.config['USER_INVITATION_FILE'], wallpaperFileName)
                saving_image(wallpaper, wallpaperPath)
            # Saving File ---------------------------------------- Finish

            # Insert Data ---------------------------------------- Start
            timestamp = int(round(time.time()*1000))
            invCode = str(random_string_number(6))
            invLink =  app.config['FE_URL']+"/"+userId+"/"+title
            query = INV_ADD_QUERY
            values = (userLevel, categoryId, templateId, title, wallpaper, personalData, invSett, invCode, invLink, timestamp, userId, timestamp, userId)
            DBHelper().save_data(query, values)
            # Insert Data ---------------------------------------- Finish

            # Log Activity Record ---------------------------------------- Start
            activity = f"User dengan id {userId} telah membuat undangan baru: {title}"
            query = LOG_ADD_QUERY
            values = (userId, activity, )
            DBHelper().save_data(query, values)
            # Log Activity Record ---------------------------------------- Finish

            # Return Response ======================================== 
            return success("Succeed!")
        
        except Exception as e:
            return bad_request(str(e))
    # CREATE INVITATION ============================================================ End

    # GET ALL INVITATION ============================================================ Begin
    def view_invitation():
        try:
            # Checking Data ---------------------------------------- Start
            query = INV_GET_ALL_QUERY
            result = DBHelper().execute(query)
            print(result)
            if len(result) == 0 or result == None:
                return defined_error("Belum ada invitation.", "Not Found", 404)
            # Checking Data ---------------------------------------- Finish
            
            # Response Data ---------------------------------------- Start
            response = []
            for rsl in result:
                data = {
                    "invitation_id" : rsl["id"],
                    "user_id" : rsl["user_id"],
                    "category_id" : rsl["category_id"],
                    "template_id" : rsl["template_id"],
                    "invitation_tittle" : rsl["tittle"],
                    "invitation_wallpaper" : rsl["wallpaper"],
                    "personal_data" : rsl["personal_data"],
                    "invitation_code" : rsl["code"],
                    "invitation_link" : rsl["link"],
                    "created_at": rsl["created_at"],
                    "updated_at" : rsl["updated_att"]
                }
                response.append(data)
            # Response Data ---------------------------------------- Finish
            print(response)
            
            # Return Response ======================================== 
            return success_data("Succeed!", response)
        
        except Exception as e:
            return bad_request(str(e))
    # GET ALL INVITATION ============================================================ End

    # UPDATE INVITATION ============================================================ Begin
    def edit_invitation(user_id, user_role,  datas):
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
            result = DBHelper().get_data(query, values)
            if len(result) == 0 :
                return defined_error("Kategori tidak dapat ditemukan.")
            
            ctgrCheck = vld_invitation(ctgr)
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
            return success("Succeed!")
            
        except Exception as e:
            return bad_request(str(e))
    # UPDATE INVITATION ============================================================ End

    # DELETE INVITATION ============================================================ Begin
    def delete_invitation(user_id, user_role, datas):
        try:
            # Access Validation ---------------------------------------- Start
            access, message = vld_role(user_role)
            if not access:
                return defined_error(message, "Forbidden", 403)
            # Access Validation ---------------------------------------- Finish

            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            if "category_id" not in datas:
                return parameter_error(f"Missing 'category_id' in Request Body")
            
            ctgrId = datas["category_id"].strip()
            if ctgrId == "":
                return defined_error("ID kategori tidak boleh kosong", "Defined Error", 400)
            # Checking Request Body ---------------------------------------- Finish
            
            # Checking Data ---------------------------------------- Finish
            query = INV_GET_BY_ID_QUERY
            values = (ctgrId,)
            result = DBHelper().get_data(query, values)
            if len(result) == 0 :
                return defined_error("Kategori tidak dapat ditemukan.", "Bad Request", 400)
            # Checking Data ---------------------------------------- Finish
            
            # Delete Data ---------------------------------------- Start
            timestamp = int(round(time.time()*1000))
            query = INV_DELETE_QUERY
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
            return success_data("Deleted Successfully!", result)
            
        except Exception as e:
            return bad_request(str(e))
    # DELETE INVITATION ============================================================ End

    # GET DETAIL INVITATION ============================================================ Begin
    def view_detail_invitation(user_role, datas):
        try:
            # Access Validation ---------------------------------------- Start
            print(user_role)
            access, message = vld_role(user_role)
            if not access:
                return defined_error(message, "Forbidden", 403)
            # Access Validation ---------------------------------------- Finish

            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            if "category_id" not in datas:
                return parameter_error(f"Missing 'category_id' in Request Body")
            
            ctgrId = datas["category_id"].strip()
            if ctgrId == "":
                return defined_error("ID kategori tidak boleh kosong", "Defined Error", 400)
            # Checking Request Body ---------------------------------------- Finish
            
            # Checking Data ---------------------------------------- Start
            query = CTGR_GET_BY_ID_QUERY
            values = (ctgrId,)
            result = DBHelper().get_data(query, values)
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
            return success_data("Succeed!", response)
        
        except Exception as e:
            return bad_request(str(e))
    # GET DETAIL INVITATION ============================================================ End

    # GET ROW-COUNT INVITATION ============================================================ Begin
    def get_count_invitation(user_id, user_role):
        try:
            # Get Data By Role ---------------------------------------- Start
            if user_role == "ADMIN":
                print("ke admin")
                query = INV_GET_ALL_QUERY
                result = DBHelper().get_count_data(query)
            elif user_role == "USER":
                print("ke user")
                query = INV_GET_BY_USR_QUERY
                values = (user_id, 2, )
                result = DBHelper().get_count_filter_data(query, values)
            # Get Data By Role ---------------------------------------- Finish

            # Checking Data ---------------------------------------- Start
            if result == 0 or result == None :
                return defined_error("Number of invitations not found.")
            # Checking Data ---------------------------------------- Finish
            
            # Response Data ---------------------------------------- Start
            response = {
                "invitation_count" : result
            }
            # Response Data ---------------------------------------- Finish

            # Return Response ======================================== 
            return success_data("Successed!", response)
        
        except Exception as e:
            return bad_request(str(e))
    # GET ROW-COUNT INVITATION ============================================================ End
# CATEGORY MODEL CLASS ============================================================ End