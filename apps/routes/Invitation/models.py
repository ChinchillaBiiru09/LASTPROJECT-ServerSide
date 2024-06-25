from ...utilities.responseHelper import *
from ...utilities.dbHelper import DBHelper
from ...utilities.queries import *
from ...utilities.validator import vld_role, vld_invitation
from ...utilities.utils import random_number, saving_image, split_date_time,random_string_number

from flask import request, current_app as app
from werkzeug.utils import secure_filename
from datetime import datetime

import time, os, json


# INVITATION MODEL CLASS ============================================================ Begin
class InvitationModels():
    # CREATE INVITATION ============================================================ Begin
    # Clear
    def add_invitation(user_id, user_role, datas):
        try:
            # Access Validation ---------------------------------------- Start
            accLevel = 2  # 1 = Admin | 2 = User
            access = vld_role(user_role)
            if access: # Access = True -> Admin
                return authorization_error()
            # Access Validation ---------------------------------------- Finish

            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            requiredData = ["category_id", "template_id", "title", "wallpaper", "personal_data", "inv_setting"]
            for req in requiredData:
                if req not in datas:
                    return parameter_error(f"Missing {req} in Request Body.")
            # Checking Request Body ---------------------------------------- Finish

            # Initialize Request Data ---------------------------------------- Start
            categoryId = datas["category_id"]
            templateId = datas["template_id"]
            title = datas["title"].strip()
            wallpaper = datas["wallpaper"]
            personalData = datas["personal_data"]
            invSett = datas["inv_setting"]
            # Initialize Request Data ---------------------------------------- Finish
            
            # Data Validation ---------------------------------------- Start
            invCheck, personalData, invCode = vld_invitation(categoryId, templateId, title, personalData)
            if len(invCheck) != 0:
                return defined_error(invCheck, "Bad Request", 400)
            # Data Validation ---------------------------------------- Finish
            
            # Saving File ---------------------------------------- Start
            # wallpaper
            wallpaperFileName = ""
            if wallpaper != "":
                wallpaperFileName = secure_filename(time.strftime("%Y-%m-%d %H:%M:%S")+"_"+invCode+"_wallpaper.jpg")
                wallpaperPath = os.path.join(app.config['USER_INVITATION_FILE'], wallpaperFileName)
                saving_image(wallpaper, wallpaperPath)
            # Saving File ---------------------------------------- Finish

            # Insert Data ---------------------------------------- Start
            timestamp = int(round(time.time()*1000))
            titlelink = title.replace(' ', '-')
            invLink =  app.config['FE_URL']+"/"+invCode+"/"+titlelink
            personalData = json.dumps(personalData)
            invSett = json.dumps(invSett)
            query = INV_ADD_QUERY
            values = (accLevel, user_id, categoryId, templateId, title, wallpaperFileName, personalData, invSett, invCode, invLink, timestamp, user_id, timestamp, user_id)
            DBHelper().save_data(query, values)
            # Insert Data ---------------------------------------- Finish

            # Log Activity Record ---------------------------------------- Start
            activity = f"User dengan id {user_id} telah membuat undangan baru: {title}."
            query = LOG_ADD_QUERY
            values = (user_id, accLevel, activity, timestamp, )
            DBHelper().save_data(query, values)
            # Log Activity Record ---------------------------------------- Finish

            # Return Response ======================================== 
            return success(statusCode=201)
        
        except Exception as e:
            return bad_request(str(e))
    # CREATE INVITATION ============================================================ End

    # GET ALL INVITATION ============================================================ Begin
    # Clear
    def view_invitation(user_id, user_role, datas):
        try:
            # Set Level Access ---------------------------------------- Start
            access = vld_role(user_role) # Access = True -> Admin
            accLevel = 1 if access else 2 # 1 = Admin | 2 = User
            # Set Level Access ---------------------------------------- Finish

            # Checking Request Body ---------------------------------------- Start
            if len(datas) != 0:
                if "user_id" not in datas:
                    return parameter_error("Missing 'user_id' in request body.")
                
                user_id = datas["user_id"]
                accLevel = 2
                if user_id == "":
                    return defined_error("Id user tidak boleh kosong.", "Defined Error", 499)
            # Checking Request Body ---------------------------------------- Finish
            
            # Checking Data ---------------------------------------- Start
            if access:
                query = INV_GET_ALL_QUERY
                result = DBHelper().execute(query)
            else:
                query = INV_GET_USER_ID_QUERY
                values = (user_id, accLevel, )
                result = DBHelper().get_data(query, values)
            
            if len(result) < 1 or result is None:
                return not_found("Data undangan tidak dapat ditemukan.")
            # Checking Data ---------------------------------------- Finish
            
            # Get Data Category ---------------------------------------- Start
            query = CTGR_GET_ALL_QUERY
            resultCtgr = DBHelper().execute(query)
            if len(resultCtgr) < 1 or resultCtgr is None:
                return not_found("Data kategori tidak dapat ditemukan.")
            # Get Data Category ---------------------------------------- Finish

            # Join Data ---------------------------------------- Start
            for invitation in result:
                for category in resultCtgr:
                    if invitation["category_id"] == category["id"]:
                        invitation["category"] = category["category"]
            # Join Data ---------------------------------------- Finish

            # Generate File URL ---------------------------------------- Start
            if len(result) >= 1:
                detailRequestURL = str(request.url).find('?')
                if detailRequestURL != -1:
                    index = detailRequestURL
                    request.url = request.url[:index]
            for item in result:
                item["wallpaper"] = f"{request.url_root}invitation/media/{item['wallpaper']}"
            # Generate File URL ---------------------------------------- Finish
            
            # Response Data ---------------------------------------- Start
            query1 = GUEST_GET_BY_CODE_QUERY
            query2 = GRTG_GET_BY_CODE_QUERY
            response = []
            for rsl in result:
                values = (rsl['code'], )
                guest = DBHelper().get_data(query1, values)
                greeting = DBHelper().get_data(query2, values)
                createdAt = split_date_time(datetime.fromtimestamp(rsl['created_at']/1000))
                updatedAt = split_date_time(datetime.fromtimestamp(rsl['updated_at']/1000))
                data = {
                    "invitation_id" : rsl["id"],
                    "user_id" : rsl["user_id"],
                    "category_id" : rsl["category_id"],
                    "category" : rsl["category"],
                    "template_id" : rsl["template_id"],
                    "invitation_title" : rsl["title"],
                    "invitation_wallpaper" : rsl["wallpaper"],
                    "personal_data" : rsl["personal_data"],
                    "invitation_code" : rsl["code"],
                    "invitation_link" : rsl["link"],
                    "guest_count" : guest[0]["count"],
                    "greeting_count" : greeting[0]["count"],
                    "created_at": createdAt,
                    "updated_at" : updatedAt
                }
                response.append(data)
            # Response Data ---------------------------------------- Finish
            
            # Return Response ======================================== 
            return success_data(response)
        
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
    # Clear
    def get_count_invitation(user_id, user_role):
        try:
            # Get Data By Role ---------------------------------------- Start
            access = vld_role(user_role)
            if access: # Access = True -> Admin
                query = INV_GET_ALL_QUERY
                result = DBHelper().get_count_data(query)
            else:
                query = INV_GET_BY_USR_QUERY
                values = (user_id, 2, )
                result = DBHelper().get_count_filter_data(query, values)
            # Get Data By Role ---------------------------------------- Finish

            # Checking Data ---------------------------------------- Start
            if result < 1 or result is None :
                return defined_error("Number of invitations not found.")
            # Checking Data ---------------------------------------- Finish
            
            # Response Data ---------------------------------------- Start
            response = {
                "invitation_count" : result
            }
            # Response Data ---------------------------------------- Finish

            # Return Response ======================================== 
            return success_data(response)
        
        except Exception as e:
            return bad_request(str(e))
    # GET ROW-COUNT INVITATION ============================================================ End
# CATEGORY MODEL CLASS ============================================================ End