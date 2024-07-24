from ...utilities.responseHelper import *
from ...utilities.dbHelper import DBHelper
from ...utilities.queries import *
from ...utilities.validator import vld_template, vld_role
from ...utilities.utils import random_number, saving_image, saving_file, split_date_time
from ..Category.models import CategoryModels

from flask import request, current_app as app
from werkzeug.utils import secure_filename
from datetime import datetime

import time, os

# TEMPLATE MODEL CLASS ============================================================ Begin
class TemplateModels():
    # CREATE TEMPLATE ============================================================ Begin
    # Clear
    def add_template(user_id, user_role, datas):
        try:
            # Access Validation ---------------------------------------- Start
            access = vld_role(user_role) # Access = True -> Admin
            accLevel = 1 if access else authorization_error()
            # Access Validation ---------------------------------------- Finish

            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            requiredData = ["title", "thumbnail", "css_file", "js_file",
                             "wallpaper_1", "wallpaper_2", "category_id"]
            for req in requiredData:
                if req not in datas:
                    return parameter_error(f"Missing {req} in Request Body.")
            # Checking Request Body ---------------------------------------- Finish
            
            # Initialize Data Input ---------------------------------------- Start
            title = datas["title"].strip()
            thumbnail = datas["thumbnail"]
            css = datas["css_file"]
            js = datas["js_file"]
            wallpaper1 = datas["wallpaper_1"]
            wallpaper2 = datas["wallpaper_2"]
            ctgr_id = datas["category_id"]
            # Initialize Data Input ---------------------------------------- Finish

            # Data Validation ---------------------------------------- Start
            tmpltCheck, randomNumber = vld_template(title, thumbnail, css, js, wallpaper1, wallpaper2, ctgr_id)
            if len(tmpltCheck) != 0:
                return defined_error(tmpltCheck, "Bad Request", 400)
            # Data Validation ---------------------------------------- Finish

            # Saving File ---------------------------------------- Start
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
            # Wallpaper 1
            wallpFileName1 = secure_filename(time.strftime("%Y-%m-%d %H:%M:%S")+"_"+randomNumber+"_wallpaper_1.jpg")
            wallpPath = os.path.join(app.config['TEMPLATE_WALLPAPER_PHOTOS'], wallpFileName1)
            saving_image(wallpaper1, wallpPath)
            # wallpaper 2
            wallpFileName2 = ""
            if wallpaper2 != "":
                wallpFileName2 = secure_filename(time.strftime("%Y-%m-%d %H:%M:%S")+"_"+randomNumber+"_wallpaper_2.jpg")
                wallpPath = os.path.join(app.config['TEMPLATE_WALLPAPER_PHOTOS'], wallpFileName2)
                saving_image(wallpaper2, wallpPath)
            # Saving File ---------------------------------------- Finish
            
            # Insert Data ---------------------------------------- Start
            timestamp = int(round(time.time()*1000))
            query = TMPLT_ADD_QUERY
            values = (title, thumbFileName, cssFileName, jsFileName, wallpFileName1, wallpFileName2, ctgr_id, timestamp, user_id, timestamp, user_id)
            DBHelper().save_data(query, values)
            # Insert Data ---------------------------------------- Finish

            # Log Activity Record ---------------------------------------- Start
            activity = f"Admin dengan id {user_id} menambahkan template baru: {title}."
            query = LOG_ADD_QUERY
            values = (user_id, accLevel, activity, timestamp, )
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
            if len(result) < 1:
                return not_found("Data template tidak dapat ditemukan.")
            # Checking Data ---------------------------------------- Finish
            
            # Get Data Category ---------------------------------------- Start
            query = CTGR_GET_ALL_QUERY
            resultCtgr = DBHelper().execute(query)
            if len(resultCtgr) < 1:
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
                item["thumb_fname"] = item['thumbnail']
                item["thumbnail"] = f"{request.url_root}template/media/thumbnail/{item['thumbnail']}"
                item["css_fname"] = item['css_file']
                item["css_file"] = f"{request.url_root}template/media/css/{item['css_file']}"
                item["js_fname"] = item['js_file']
                item["js_file"] = f"{request.url_root}template/media/js/{item['js_file']}"
                item["wp_fname"] = item['wallpaper']
                item["wallpaper"] = f"{request.url_root}template/media/wallpaper/{item['wallpaper']}"
                item["wp2_fname"] = item['wallpaper_2']
                item["wallpaper_2"] = f"{request.url_root}template/media/wallpaper/{item['wallpaper_2']}"
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
                    "thumb_fname" : rsl["thumb_fname"],
                    "css_file" : rsl["css_file"],
                    "css_fname" : rsl["css_fname"],
                    "js_file" : rsl["js_file"],
                    "js_fname" : rsl["js_fname"],
                    "wallpaper": rsl["wallpaper"],
                    "wp_fname": rsl["wp_fname"],
                    "wallpaper_2": rsl["wallpaper_2"],
                    "wp2_fname": rsl["wp2_fname"],
                    "category_id" : rsl["category_id"],
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
            
            requiredData = ["template_id", "title", "thumbnail", "css_file", "js_file", 
                            "wallpaper_1", "wallpaper_2", "category_id"]
            for req in requiredData:
                if req not in datas:
                    return parameter_error(f"Missing {req} in Request Body.")
            # Checking Request Body ---------------------------------------- Finish
            
            # Initialize Data Input ---------------------------------------- Start
            tempId = datas["template_id"]
            title = datas["title"].strip()
            css = datas["css_file"]
            js = datas["js_file"]
            thumbnail = datas["thumbnail"]
            wallpaper1 = datas["wallpaper_1"]
            wallpaper2 = datas["wallpaper_2"]
            catgId = datas["category_id"]
            # Initialize Data Input ---------------------------------------- Finish
            
            # Data Validation ---------------------------------------- Start
            query = TMPLT_GET_BY_ID_QUERY
            values = (tempId,)
            result = DBHelper().get_data(query, values)
            if len(result) < 1 :
                return not_found(f"Template dengan Id {tempId} tidak dapat ditemukan.")
            
            ctgrCheck, randomNumber = vld_template(title, thumbnail, css, js, wallpaper1, wallpaper2, catgId, False)
            if len(ctgrCheck) != 0:
                return defined_error(ctgrCheck, "Bad Request", 400)
            # Data Validation ---------------------------------------- Finish

            # Saving File ---------------------------------------- Start
            result = result[0]
            print(datas)
            if thumbnail != result['thumbnail']:
                print("Masuk?")
                # Thumbnail
                thumbFileName = secure_filename(time.strftime("%Y-%m-%d %H:%M:%S")+"_"+randomNumber+"_thumbnail.jpg")
                thumbPath = os.path.join(app.config['TEMPLATE_THUMBNAIL_PHOTOS'], thumbFileName)
                saving_image(thumbnail, thumbPath)
            else:
                thumbFileName = thumbnail

            if css != result['css_file']:
                # CSS
                cssFileName = secure_filename(time.strftime("%Y-%m-%d %H:%M:%S")+"_"+randomNumber+"_style.css")
                cssPath = os.path.join(app.config['TEMPLATE_CSS_FILE'], cssFileName)
                saving_file(css, cssPath)
            else:
                cssFileName = css
                
            if js != result['js_file']:
                # JS
                jsFileName = ""
                if js != "":
                    jsFileName = secure_filename(time.strftime("%Y-%m-%d %H:%M:%S")+"_"+randomNumber+"_script.js")
                    jsPath = os.path.join(app.config['TEMPLATE_JS_FILE'], jsFileName)
                    saving_file(js, jsPath)
            else:
                jsFileName = js
                    
            if wallpaper1 != result['wallpaper']:
                # Wallpaper 1
                wallpFileName1 = secure_filename(time.strftime("%Y-%m-%d %H:%M:%S")+"_"+randomNumber+"_wallpaper_1.jpg")
                wallpPath = os.path.join(app.config['TEMPLATE_WALLPAPER_PHOTOS'], wallpFileName1)
                saving_image(wallpaper1, wallpPath)
            else:
                wallpFileName1 = wallpaper1
                
            if wallpaper2 != result['wallpaper_2']:
                # wallpaper 2
                wallpFileName2 = secure_filename(time.strftime("%Y-%m-%d %H:%M:%S")+"_"+randomNumber+"_wallpaper_2.jpg")
                wallpPath = os.path.join(app.config['TEMPLATE_WALLPAPER_PHOTOS'], wallpFileName2)
                saving_image(wallpaper2, wallpPath)
            else:
                wallpFileName2 = wallpaper2
            # Saving File ---------------------------------------- Finish
            
            # Update Data ---------------------------------------- Start
            timestamp = int(round(time.time()*1000))
            query = TMPLT_UPDATE_QUERY
            values = (title, thumbFileName, cssFileName, jsFileName, wallpFileName1, wallpFileName2, catgId, timestamp, user_id, tempId)
            DBHelper().save_data(query, values)
            # Update Data ---------------------------------------- Finish

            # Log Activity Record ---------------------------------------- Start
            activity = f"Admin dengan Id {user_id} mengubah template {tempId}: {result['title']}."
            query = LOG_ADD_QUERY
            values = (user_id, 1, activity, timestamp, )
            DBHelper().save_data(query, values)
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
            result = DBHelper().get_data(query, values)
            if len(result) == 0 :
                return not_found(f"Template dengan Id {tempId} tidak dapat ditemukan.")
            # Data Validation ---------------------------------------- Finish
            
            # Delete Data ---------------------------------------- Start
            timestamp = int(round(time.time()*1000))
            query = TMPLT_DELETE_QUERY
            values = (timestamp, user_id, tempId)
            DBHelper().save_data(query, values)
            # Delete Data ---------------------------------------- Finish

            # Delete Join Data ---------------------------------------- Start
            # Invitation
            query = INV_GET_BY_TEMP_QUERY
            values = (tempId, )
            invitation = DBHelper().get_data(query, values)
            if len(invitation) > 0:
                query = INV_DELETE_TEMP_QUERY
                values = (timestamp, user_id, tempId, )
                DBHelper().save_data(query, values)
            
                # Guest
                for inv in invitation:
                    invCode = inv['code']
                    query = GUEST_GET_BY_CODE_QUERY
                    values = (invCode, )
                    guest = DBHelper().get_count_filter_data(query, values)
                    if guest > 0:
                        query = GUEST_DELETE_INV_QUERY
                        values = (timestamp, user_id, invCode, )
                        DBHelper().save_data(query, values)

                    # Greeting
                    query = GRTG_GET_BY_CODE_QUERY
                    values = (invCode, )
                    greeting = DBHelper().get_count_filter_data(query, values)
                    if greeting > 0:
                        query = GRTG_DELETE_INV_QUERY
                        values = (timestamp, user_id, invCode, )
                        DBHelper().save_data(query, values)
            # Delete Join Data ---------------------------------------- Finish

            # Log Activity Record ---------------------------------------- Start
            activity = f"Admin dengan id {user_id} menghapus template {tempId}."
            query = LOG_ADD_QUERY
            values = (user_id, 1, activity, timestamp, )
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
            if len(result) < 1 :
                return not_found(f"Data template dengan Id {tempId} tidak dapat ditemukan.")
            # Checking Data ---------------------------------------- Finish

            # Get & Join Data Category ---------------------------------------- Start
            template = result[0]
            query = CTGR_GET_BY_ID_QUERY
            values = (template['category_id'], )
            category = DBHelper().get_data(query, values)
            if len(result) < 1 :
                return not_found(f"Data kategori dengan Id {template['category_id']} tidak dapat ditemukan.")
            template["category"] = category[0]["category"]
            # Get & Join Data Category ---------------------------------------- Finish

            # Generate File URL ---------------------------------------- Start
            if len(result) >= 1:
                detailRequestURL = str(request.url).find('?')
                if detailRequestURL != -1:
                    index = detailRequestURL
                    request.url = request.url[:index]
            
            template["thumb_fname"] = template['thumbnail']
            template["thumbnail"] = f"{request.url_root}template/media/thumbnail/{template['thumbnail']}"
            template["css_fname"] = template['css_file']
            template["css_file"] = f"{request.url_root}template/media/css/{template['css_file']}"
            template["js_fname"] = template['js_file']
            template["js_file"] = f"{request.url_root}template/media/js/{template['js_file']}"
            template["wp_fname"] = template['wallpaper']
            template["wallpaper"] = f"{request.url_root}template/media/wallpaper/{template['wallpaper']}"
            template["wp2_fname"] = template['wallpaper_2']
            template["wallpaper_2"] = f"{request.url_root}template/media/wallpaper/{template['wallpaper_2']}"
            # Generate File URL ---------------------------------------- Finish
            
            # Response Data ---------------------------------------- Start
            template['created_at'] = split_date_time(datetime.fromtimestamp(template['created_at']/1000))
            template['updated_at'] = split_date_time(datetime.fromtimestamp(template['updated_at']/1000))
            response = {
                    "template_id" : template["id"],
                    "title" : template["title"].title(),
                    "thumbnail" : template["thumbnail"],
                    "thumb_fname" : template["thumb_fname"],
                    "css_file" : template["css_file"],
                    "css_fname" : template["css_fname"],
                    "js_file" : template["js_file"],
                    "js_fname" : template["js_fname"],
                    "wallpaper": template["wallpaper"],
                    "wp_fname": template["wp_fname"],
                    "wallpaper_2": template["wallpaper_2"],
                    "wp2_fname": template["wp2_fname"],
                    "category_id" : template["category_id"],
                    "category" : template["category"],
                    "created_at" : template['created_at'],
                    "updated_at" : template['updated_at']
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
# TEMPLATE MODEL CLASS ============================================================ End
