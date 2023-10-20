from ...utilities.responseHelper import invalid_params, parameter_error, defined_error, bad_request, success, success_data
from ...utilities.dbHelper import DBHelper
from ...utilities.queries import *
from ...utilities.validator import vld_template, vld_role
from ...utilities.utils import random_number, saving_file

from flask import request, current_app as app
from werkzeug.utils import secure_filename
from time import strftime

import time, os

# CATEGORY MODEL CLASS ============================================================ Begin
class TemplateModels():
    # CREATE CATEGORY ============================================================ Begin
    def add_template(user_id, user_role, datas):
        try:
            # Access Validation ---------------------------------------- Start
            access, message = vld_role(user_role)
            if not access:
                return defined_error(message, "Forbidden", 403)
            # Access Validation ---------------------------------------- Finish

            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            requiredData = ["tmplt_title", "tmplt_thumbnail", "css_file", "js_file", "tmplt_wallpaper", "category_id"]
            if requiredData not in datas:
                return parameter_error(f"Missing {requiredData} in Request Body")
            # Checking Request Body ---------------------------------------- Finish
            
            # Variable Data Input ---------------------------------------- Start
            title = datas["tmplt_title"].title().strip()
            thumbnail = datas["tmplt_thumbnail"]
            css = datas["css_file"]
            js = datas["js_file"]
            wallpaper = datas["tmplt_wallpaper"]
            ctgr_id = datas["category_id"]
            # Variable Data Input ---------------------------------------- Finish

            # Data Validation ---------------------------------------- Start
            ctgrCheck = vld_template(title, thumbnail, css, wallpaper)
            if len(ctgrCheck) != 0:
                return defined_error(ctgrCheck, "Bad Request", 400)
            # Data Validation ---------------------------------------- Finish

            # Saving File ---------------------------------------- Start
            randomNumber = str(random_number(5))
            # Thumbnail
            thumbFileName = secure_filename(strftime("%Y-%m-%d %H:%M:%S")+"_"+randomNumber+"_thumbnail.jpg")
            thumbPath = os.path.join(app.config['TEMPLATE_THUMBNAIL_PHOTOS'], thumbFileName)
            saving_file(thumbnail, thumbPath)
            # CSS
            cssFileName = secure_filename(strftime("%Y-%m-%d %H:%M:%S")+"_"+randomNumber+"_style.css")
            cssPath = os.path.join(app.config['TEMPLATE_CSS_FILE'], cssFileName)
            saving_file(css, cssPath)
            # JS
            jsPath = ""
            if js != "":
                jsFileName = secure_filename(strftime("%Y-%m-%d %H:%M:%S")+"_"+randomNumber+"_script.js")
                jsPath = os.path.join(app.config['TEMPLATE_JS_FILE'], jsFileName)
                saving_file(js, jsPath)
            # Wallpaper
            wallpFileName = secure_filename(strftime("%Y-%m-%d %H:%M:%S")+"_"+randomNumber+"_wallpaper.jpg")
            wallpPath = os.path.join(app.config['TEMPLATE_WALLPAPER_PHOTOS'], wallpFileName)
            saving_file(wallpaper, wallpPath)
            # Saving File ---------------------------------------- Finish
            
            # Insert Data ---------------------------------------- Start
            timestamp = int(round(time.time()*1000))
            query = TMPLT_ADD_QUERY
            values = (title, thumbPath, cssPath, jsPath, wallpPath, ctgr_id, timestamp, user_id, timestamp, user_id)
            DBHelper().save_data(query, values)
            # Insert Data ---------------------------------------- Finish

            # Log Activity Record ---------------------------------------- Start
            activity = f"Admin dengan id {user_id} menambahkan template baru: {title}"
            query = LOG_ADD_QUERY
            values = (user_id, activity, )
            DBHelper().save_data(query, values)
            # Log Activity Record ---------------------------------------- Finish

            # Return Response ======================================== 
            return success("Successed!")
        
        except Exception as e:
            return bad_request(str(e))
    # CREATE CATEGORY ============================================================ End

    # GET ALL CATEGORY ============================================================ Begin
    def view_template(data):
        try:
            # Checking Data ---------------------------------------- Start
            query = TMPLT_GET_QUERY
            result = DBHelper().execute(query)
            if len(result) == 0 or result == None:
                return defined_error("Belum ada template.", "Bad Request", 400)
            # Checking Data ---------------------------------------- Finish

            # Get Data Category ---------------------------------------- Start
            # query = CTGR_GET_QUERY
            # resultCtgr = DBHelper().execute(query)
            # if len(resultCtgr) == 0 or resultCtgr == None:
            #     return defined_error("Kategori tidak terdaftar.", "Bad Request", 400)
            # Get Data Category ---------------------------------------- Finish

            # Join Data ---------------------------------------- Start
            # Join Data ---------------------------------------- Finish
            
            # Response Data ---------------------------------------- Start
            response = []
            for rsl in result:
                value = (rsl["category_id"],)
                resultCtgr = DBHelper().get_data(query, value)
                category = ""
                if resultCtgr != 0:
                    category = resultCtgr["category"]
                data = {
                    "template_id" : rsl["id"],
                    "title" : rsl["title"],
                    "thumbnail" : f"{request.url_root}produk/media/{rsl['thumbnail']}",
                    "category" : category,
                    "created_at" : rsl["created_at"],
                    "updated_at" : rsl["updated_at"]
                }
                response.append(data)
            # Response Data ---------------------------------------- Finish
            
            # Return Response ======================================== 
            return success_data("Successed!", response)
        
        except Exception as e:
            return bad_request(str(e))
    # GET ALL CATEGORY ============================================================ End

    # UPDATE CATEGORY ============================================================ Begin
    def edit_template(user_id, user_role, datas):
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
    def delete_template(user_id, user_role, datas):
        
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

    # GET DETAIL CATEGORY ============================================================ Begin
    def view_detail_template(datas):
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
# CATEGORY MODEL CLASS ============================================================ End