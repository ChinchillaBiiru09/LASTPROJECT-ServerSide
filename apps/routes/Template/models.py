from ...utilities.responseHelper import *
from ...utilities.dbHelper import DBHelper
from ...utilities.queries import *
from ...utilities.validator import vld_template, vld_role
from ...utilities.utils import random_number, saving_image, saving_file, split_date_time

from flask import request, current_app as app
from werkzeug.utils import secure_filename
from datetime import datetime

import time, os, base64

# TEMPLATE MODEL CLASS ============================================================ Begin
class TemplateModels():
    # CREATE TEMPLATE ============================================================ Begin
    def add_template(user_id, user_role, datas):
        try:
            # Access Validation ---------------------------------------- Start
            access = vld_role(user_role)
            if not access: # Access = True -> Admin
                return authorization_error()
            # Access Validation ---------------------------------------- Finish

            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            requiredData = ["tmplt_title", "tmplt_thumbnail", "css_file", "js_file", "tmplt_wallpaper", "category_id"]
            for req in requiredData:
                if req not in datas:
                    return parameter_error(f"Missing {req} in Request Body.")
            # Checking Request Body ---------------------------------------- Finish
            
            # Initialize Data Input ---------------------------------------- Start
            title = datas["tmplt_title"].strip()
            thumbnail = datas["tmplt_thumbnail"]
            css = datas["css_file"]
            js = datas["js_file"]
            wallpaper = datas["tmplt_wallpaper"]
            ctgr_id = datas["category_id"]
            # Initialize Data Input ---------------------------------------- Finish

            # Data Validation ---------------------------------------- Start
            tmpltCheck = vld_template(title, thumbnail, css, wallpaper)
            if len(tmpltCheck) != 0:
                return defined_error(tmpltCheck, "Bad Request", 400)
            # Data Validation ---------------------------------------- Finish

            # Saving File ---------------------------------------- Start
            randomNumber = str(random_number(5))
            # Thumbnail
            thumbFileName = secure_filename(time.strftime("%Y-%m-%d %H:%M:%S")+"_"+randomNumber+"_thumbnail.jpg")
            thumbPath = os.path.join(app.config['TEMPLATE_THUMBNAIL_PHOTOS'], thumbFileName)
            saving_image(thumbnail, thumbPath)
            # CSS
            cssFileName = secure_filename(time.strftime("%Y-%m-%d %H:%M:%S")+"_"+randomNumber+"_style.css")
            cssPath = os.path.join(app.config['TEMPLATE_CSS_FILE'], cssFileName)
            saving_file(css, cssPath)
            # JS
            jsFileName = ""
            if js != "":
                jsFileName = secure_filename(time.strftime("%Y-%m-%d %H:%M:%S")+"_"+randomNumber+"_script.js")
                jsPath = os.path.join(app.config['TEMPLATE_JS_FILE'], jsFileName)
                saving_file(js, jsPath)
            # Wallpaper
            wallpFileName = secure_filename(time.strftime("%Y-%m-%d %H:%M:%S")+"_"+randomNumber+"_wallpaper.jpg")
            wallpPath = os.path.join(app.config['TEMPLATE_WALLPAPER_PHOTOS'], wallpFileName)
            saving_file(wallpaper, wallpPath)
            # Saving File ---------------------------------------- Finish
            
            # Insert Data ---------------------------------------- Start
            timestamp = int(round(time.time()*1000))
            query = TMPLT_ADD_QUERY
            values = (title, thumbFileName, cssFileName, jsFileName, wallpFileName, ctgr_id, timestamp, user_id, timestamp, user_id)
            DBHelper().save_data(query, values)
            # Insert Data ---------------------------------------- Finish

            # Log Activity Record ---------------------------------------- Start
            activity = f"Admin dengan id {user_id} menambahkan template baru: {title}."
            query = LOG_ADD_QUERY
            values = (user_id, activity, )
            DBHelper().save_data(query, values)
            # Log Activity Record ---------------------------------------- Finish

            # Return Response ======================================== 
            return success(statusCode=201)
        
        except Exception as e:
            return bad_request(str(e))
    # CREATE TEMPLATE ============================================================ End

    # GET ALL TEMPLATE ============================================================ Begin
    def view_template():
        try:
            # Checking Data ---------------------------------------- Start
            query = TMPLT_GET_ALL_QUERY
            result = DBHelper().execute(query)
            if len(result) < 1 or result is None:
                return not_found("Data template tidak dapat ditemukan.")
            # Checking Data ---------------------------------------- Finish
            
            # Get Data Category ---------------------------------------- Start
            query = CTGR_GET_ALL_QUERY
            resultCtgr = DBHelper().execute(query)
            if len(resultCtgr) < 1 or resultCtgr is None:
                return not_found("Data kategori tidak dapat ditemukan.")
            # Get Data Category ---------------------------------------- Finish

            # Join Data ---------------------------------------- Start
            for template in result:
                for category in resultCtgr:
                    if template["category_id"] == category["id"]:
                        template["category"] = category["category"]
            # Join Data ---------------------------------------- Finish

            # Generate File URL ---------------------------------------- Start
            if len(result) >= 1:
                detailRequestURL = str(request.url).find('?')
                if detailRequestURL != -1:
                    index = detailRequestURL
                    request.url = request.url[:index]
            for item in result:
                item["thumbnail"] = f"{request.url_root}template/media/thumbnail/{item['thumbnail']}"
                item["css_file"] = f"{request.url_root}template/media/css/{item['css_file']}"
                item["js_file"] = f"{request.url_root}template/media/js/{item['js_file']}"
                item["wallpaper"] = f"{request.url_root}template/media/wallpaper/{item['wallpaper']}"
            # Generate File URL ---------------------------------------- Finish
            
            # Response Data ---------------------------------------- Start
            response = []
            for rsl in result:
                createdAt = split_date_time(datetime.fromtimestamp(rsl['created_at']/1000))
                updatedAt = split_date_time(datetime.fromtimestamp(rsl['updated_at']/1000))
                data = {
                    "template_id" : rsl["id"],
                    "title" : rsl["title"],
                    "thumbnail" : rsl["thumbnail"],
                    "css_file" : rsl["css_file"],
                    "js_file" : rsl["js_file"],
                    "wallpaper": rsl["wallpaper"],
                    "category" : rsl["category"],
                    "created_at" : createdAt,
                    "updated_at" : updatedAt
                }
                response.append(data)
            # Response Data ---------------------------------------- Finish
            
            # Return Response ======================================== 
            return success_data(response)
        
        except Exception as e:
            return bad_request(str(e))
    # GET ALL TEMPLATE ============================================================ End

    # UPDATE TEMPLATE ============================================================ Begin
    def edit_template(user_id, user_role, datas):
        try:
            # Access Validation ---------------------------------------- Start
            access = vld_role(user_role)
            if not access: # Access = True -> Admin
                return authorization_error()
            # Access Validation ---------------------------------------- Finish

            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            requiredData = ["template_id", "template_title", "template_thumbnail", "css_file", "js_file", "template_wallpaper", "category_id"]
            for req in requiredData:
                if req not in datas:
                    return parameter_error(f"Missing {req} in Request Body.")
            # Checking Request Body ---------------------------------------- Finish
            
            # Initialize Data Input ---------------------------------------- Start
            tempId = datas["template_id"]
            title = datas["title"].strip()
            thumbnail = datas["thumbnail"]
            wallpaper = datas["wallpaper"]
            cssFile = datas["css_file"]
            jsFile = datas["title"]
            catgId = datas["category_id"]
            # Initialize Data Input ---------------------------------------- Finish
            
            # Data Validation ---------------------------------------- Start
            query = TMPLT_GET_BY_ID_QUERY
            values = (tempId,)
            result = DBHelper.get_count_filter_data(query, values)
            if result == 0 :
                return not_found(f"Template dengan Id {tempId} tidak dapat ditemukan.")
            
            ctgrCheck, result = vld_template(title, thumbnail, cssFile, wallpaper)
            if len(ctgrCheck) != 0:
                return defined_error(ctgrCheck, "Bad Request", 400)
            # Data Validation ---------------------------------------- Finish
            
            # Update Data ---------------------------------------- Start
            timestamp = int(round(time.time()*1000))
            query = TMPLT_UPDATE_QUERY
            values = (title, thumbnail, cssFile, jsFile, wallpaper, catgId, timestamp, user_id, tempId)
            # DBHelper().save_data(query, values)
            # Update Data ---------------------------------------- Finish

            # Log Activity Record ---------------------------------------- Start
            activity = f"Admin dengan Id {user_id} mengubah template {tempId}: {result[0]['title']}."
            query = LOG_ADD_QUERY
            values = (user_id, activity, )
            # DBHelper().save_data(query, values)
            # Log Activity Record ---------------------------------------- Finish

            # Return Response ======================================== 
            return success(message="Updated!")
            
        except Exception as e:
            return bad_request(str(e))
    # UPDATE TEMPLATE ============================================================ End

    # DELETE TEMPLATE ============================================================ Begin
    def delete_template(user_id, user_role, datas):
        try:
            # Access Validation ---------------------------------------- Start
            access = vld_role(user_role)
            if not access: # Access = True -> Admin
                return authorization_error()
            # Access Validation ---------------------------------------- Finish

            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            if "template_id" not in datas:
                return parameter_error("Missing 'category_id' in Request Body.")
            
            tempId = datas["template_id"]
            if tempId == "":
                return defined_error("Id template tidak boleh kosong.", "Defined Error", 499)
            # Checking Request Body ---------------------------------------- Finish
            
            # Data Validation ---------------------------------------- Start
            query = TMPLT_GET_BY_ID_QUERY
            values = (tempId,)
            result = DBHelper().get_count_filter_data(query, values)
            if result == 0 :
                return not_found(f"Template dengan Id {tempId} tidak dapat ditemukan.")
            # Data Validation ---------------------------------------- Finish
            
            # Delete Data ---------------------------------------- Start
            timestamp = int(round(time.time()*1000))
            query = TMPLT_DELETE_QUERY
            values = (timestamp, user_id, tempId)
            DBHelper().save_data(query, values)
            # Delete Data ---------------------------------------- Finish

            # Log Activity Record ---------------------------------------- Start
            activity = f"Admin dengan id {user_id} menghapus template {tempId}."
            query = LOG_ADD_QUERY
            values = (user_id, activity, )
            DBHelper().save_data(query, values)
            # Log Activity Record ---------------------------------------- Finish

            # Return Response ======================================== 
            return success(message="Deleted!")
            
        except Exception as e:
            return bad_request(str(e))
    # DELETE TEMPLATE ============================================================ End

    # GET DETAIL TEMPLATE ============================================================ Begin
    def view_detail_template(datas):
        try:
            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            if "template_id" not in datas:
                return parameter_error("Missing 'template_id' in Request Body.")
            
            tempId = datas["template_id"]
            if tempId == "":
                return defined_error("Id template tidak boleh kosong.", "Defined Error", 499)
            # Checking Request Body ---------------------------------------- Finish
            
            # Checking Data ---------------------------------------- Start
            query = TMPLT_GET_BY_ID_QUERY
            values = (tempId,)
            result = DBHelper().get_data(query, values)
            if len(result) == 0 :
                return not_found(f"Template dengan Id {tempId} tidak dapat ditemukan.")
            # Checking Data ---------------------------------------- Finish

            # Generate File URL ---------------------------------------- Start
            template = result[0]
            if len(result) >= 1:
                detailRequestURL = str(request.url).find('?')
                if detailRequestURL != -1:
                    index = detailRequestURL
                    request.url = request.url[:index]
            for item in result:
                template["thumbnail"] = f"{request.url_root}template/media/thumbnail/{template['thumbnail']}"
                template["css_file"] = f"{request.url_root}template/media/css/{template['css_file']}"
                template["js_file"] = f"{request.url_root}template/media/js/{template['js_file']}"
                template["wallpaper"] = f"{request.url_root}template/media/wallpaper/{template['wallpaper']}"
            # Generate File URL ---------------------------------------- Finish
            
            # Response Data ---------------------------------------- Start
            response = {
                "template_id" : template["id"],
                "thumbnail" : template["thumbnail"],
                "css_file" : template["css_file"],
                "js_file" : template["js_file"],
                "wallpaper" : template["wallpaper"],
                "updated_at": template["updated_at"]
            }
            # Response Data ---------------------------------------- Finish

            # Return Response ======================================== 
            return success_data(response)
        
        except Exception as e:
            return bad_request(str(e))
    # GET DETAIL TEMPLATE ============================================================ End
        
    # VIEW TEMPLATE ============================================================ Begin
    def show_template(datas):
        try:
            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            #
            
            tempId = datas["template_id"]
            if tempId == "":
                return defined_error("Id template tidak boleh kosong.", "Defined Error", 499)
            # Checking Request Body ---------------------------------------- Finish
            
            # # Checking Data ---------------------------------------- Start
            # query = TMPLT_GET_BY_ID_QUERY
            # values = (tempId,)
            # result = DBHelper.get_data(query, values)
            # if len(result) == 0 :
            #     return not_found(f"Template dengan Id {tempId} tidak dapat ditemukan.")
            # # Checking Data ---------------------------------------- Finish

            # Generate Data ---------------------------------------- Start
            # for data in result:
            #     print(data)
            # template = result[0]
            # if template["thumbnail"] != "":
            #     template["thumbnail"] = base64.b64encode(template["thumbnail"])
            # if template["css_file"] != "":
            #     template["css_file"] = base64.b64encode(template["css_file"])
            # if template["js_file"] != "":
            #     template["js_file"] = base64.b64encode(template["js_file"])
            # if template["wallpaper"] != "":
            #     template["wallpaper"] = base64.b64encode(template["wallpaper"])
            # Generate Data ---------------------------------------- Finish

            # Generate File URL ---------------------------------------- Start
            detailRequestURL = str(request.url).find('?')
            if detailRequestURL != -1:
                index = detailRequestURL
                request.url = request.url[:index]
            htmlTemplate = f"{request.url_root}template/media/html/template_1.html"
            # Generate File URL ---------------------------------------- Finish
            
            # Response Data ---------------------------------------- Start
            response = {
                "template" : htmlTemplate
            }
            # response = {
            #     "template_id" : template["id"],
            #     "thumbnail" : template["category"],
            #     "css_file" : template["css_file"],
            #     "js_file" : template["js_file"],
            #     "wallpaper" : template["wallpaper"],
            #     "updated_at": template["updated_at"]
            # }
            # Response Data ---------------------------------------- Finish

            # Return Response ======================================== 
            return success_data(response)
        
        except Exception as e:
            return bad_request(str(e))
    # VIEW TEMPLATE ============================================================ End

    # GET ROW-COUNT TEMPLATE ============================================================ Begin
    # Clear
    def get_count_template():
        try:
            # Checking Data ---------------------------------------- Start
            query = TMPLT_GET_ALL_QUERY
            result = DBHelper().get_count_data(query)
            if result < 1 or result is None :
                return not_found("Data template tidak dapat ditemukan.")
            # Checking Data ---------------------------------------- Finish
            
            # Response Data ---------------------------------------- Start
            response = {
                "template_count" : result
            }
            # Response Data ---------------------------------------- Finish

            # Return Response ======================================== 
            return success_data(response)
        
        except Exception as e:
            return bad_request(str(e))
    # GET ROW-COUNT TEMPLATE ============================================================ End

    # REQUEST TEMPLATE ============================================================ Begin
    # Clear// input data checker belum
    def create_request_template(user_id, user_role, datas):
        try:
            # Access Validation ---------------------------------------- Start
            access = vld_role(user_role)
            acclevel = 2
            if access: # Access = True -> Admin
                return authorization_error()
            # Access Validation ---------------------------------------- Finish

            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            requiredData = ["category_id", "template_design", "description", "deadline", "type"]
            for req in requiredData:
                if req not in datas:
                    return parameter_error(f"Missing {req} in Request Body.")
            # Checking Request Body ---------------------------------------- Finish
            
            # Initialize Data Input ---------------------------------------- Start
            tempDesign = datas["template_design"]
            descript = datas["description"]
            deadline = datas["deadline"]
            type = datas["type"]
            catgId = datas["category_id"]
            # Initialize Data Input ---------------------------------------- Finish

            # Data Validation ---------------------------------------- Start
            # tmpltCheck = vld_template(tempDesign, thumbnail, css, wallpaper)
            # if len(tmpltCheck) != 0:
            #     return defined_error(tmpltCheck, "Bad Request", 400)
            # Data Validation ---------------------------------------- Finish

            # Saving File ---------------------------------------- Start
            randomNumber = str(random_number(5))
            # Design Photos
            designFileName = secure_filename(time.strftime("%Y-%m-%d %H:%M:%S")+"_"+randomNumber+"_design_user_"+user_id+".jpg")
            designPath = os.path.join(app.config['TEMPLATE_REQUEST_DESIGN'], designFileName)
            saving_image(tempDesign, designPath)
            # Saving File ---------------------------------------- Finish
            
            # Insert Data ---------------------------------------- Start
            status = 0 # 0 = waiting | 1 = checked | 2 = acc | decline
            timestamp = int(round(time.time()*1000))
            query = REQ_ADD_QUERY
            values = (user_id, acclevel, catgId, designFileName, descript, deadline, type, status, timestamp, user_id, timestamp, user_id)
            DBHelper().save_data(query, values)
            # Insert Data ---------------------------------------- Finish

            # Log Activity Record ---------------------------------------- Start
            activity = f"User dengan id {user_id} mengirimkan request template baru."
            query = LOG_ADD_QUERY
            values = (user_id, acclevel, activity, timestamp, )
            DBHelper().save_data(query, values)
            # Log Activity Record ---------------------------------------- Finish

            # Return Response ======================================== 
            return success(statusCode=201)
        
        except Exception as e:
            return bad_request(str(e))
    # REQUEST TEMPLATE ============================================================ End
# TEMPLATE MODEL CLASS ============================================================ End
