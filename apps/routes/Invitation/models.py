from ...utilities.responseHelper import invalid_params, parameter_error, defined_error, bad_request, success, success_data
from ...utilities.dbHelper import DBHelper
from ...utilities.queries import *
from ...utilities.validator import vld_role, vld_invitation
from ...utilities.utils import random_number, saving_file

from flask import request, current_app as app
from werkzeug.utils import secure_filename

import time, os

# CATEGORY MODEL CLASS ============================================================ Begin
class InvitationModels():
    # CREATE CATEGORY ============================================================ Begin
    def add_invitation(user_id, user_role, datas):
        try:
            # Access Validation ---------------------------------------- Start
            access, message = vld_role(user_role)
            if not access:
                return defined_error(message, "Forbidden", 403)
            # Access Validation ---------------------------------------- Finish

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
            photo1 = datas["photo_1"]
            photo2 = datas["photo_2"]
            wallpaper = datas["wallpaper"]
            personalData = datas["personal_data"]
            invSett = datas["inv_setting"]
            # Initialize Request Data ---------------------------------------- Finish
            
            # Data Validation ---------------------------------------- Start
            ctgrCheck = vld_invitation(categoryId, title, personalData, invSett)
            if len(ctgrCheck) != 0:
                return defined_error(ctgrCheck, "Bad Request", 400)
            # Data Validation ---------------------------------------- Finish
            
            # Saving File ---------------------------------------- Start
            randomNumber = str(random_number(5))
            # Photo1
            photo1FileName = secure_filename(time.strftime("%Y-%m-%d %H:%M:%S")+"_"+randomNumber+"_photo1.jpg")
            photo1Path = os.path.join(app.config['TEMPLATE_THUMBNAIL_PHOTOS'], photo1FileName)
            saving_file(photo1, photo1Path)
            # CSS
            cssFileName = secure_filename(time.strftime("%Y-%m-%d %H:%M:%S")+"_"+randomNumber+"_style.css")
            cssPath = os.path.join(app.config['TEMPLATE_CSS_FILE'], cssFileName)
            saving_file(css, cssPath)
            # JS
            jsPath = ""
            if js != "":
                jsFileName = secure_filename(time.strftime("%Y-%m-%d %H:%M:%S")+"_"+randomNumber+"_script.js")
                jsPath = os.path.join(app.config['TEMPLATE_JS_FILE'], jsFileName)
                saving_file(js, jsPath)
            # Wallpaper
            wallpFileName = secure_filename(strftime("%Y-%m-%d %H:%M:%S")+"_"+randomNumber+"_wallpaper.jpg")
            wallpPath = os.path.join(app.config['TEMPLATE_WALLPAPER_PHOTOS'], wallpFileName)
            saving_file(wallpaper, wallpPath)
            # Saving File ---------------------------------------- Finish

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
            return success("Succeed!")
        
        except Exception as e:
            return bad_request(str(e))
    # CREATE CATEGORY ============================================================ End

    # GET ALL CATEGORY ============================================================ Begin
    def view_category():
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
            return success_data("Succeed!", response)
        
        except Exception as e:
            return bad_request(str(e))
    # GET ALL CATEGORY ============================================================ End

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
            result = DBHelper().get_data(query, values)
            if len(result) == 0 :
                return defined_error("Kategori tidak dapat ditemukan.")
            
            ctgrCheck = vld_category(ctgr)
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
            
            if "category_id" not in datas:
                return parameter_error(f"Missing 'category_id' in Request Body")
            
            ctgrId = datas["category_id"].strip()
            if ctgrId == "":
                return defined_error("ID kategori tidak boleh kosong", "Defined Error", 400)
            # Checking Request Body ---------------------------------------- Finish
            
            # Checking Data ---------------------------------------- Finish
            query = CTGR_GET_BY_ID_QUERY
            values = (ctgrId,)
            result = DBHelper().get_data(query, values)
            if len(result) == 0 :
                return defined_error("Kategori tidak dapat ditemukan.", "Bad Request", 400)
            # Checking Data ---------------------------------------- Finish
            
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
            return success_data("Deleted Successfully!", result)
            
        except Exception as e:
            return bad_request(str(e))
    # DELETE CATEGORY ============================================================ End

    # GET DETAIL CATEGORY ============================================================ Begin
    def view_detail_category(user_role, datas):
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
    # GET DETAIL CATEGORY ============================================================ End
# CATEGORY MODEL CLASS ============================================================ End