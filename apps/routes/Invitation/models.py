from ...utilities.responseHelper import *
from ...utilities.dbHelper import DBHelper
from ...utilities.queries import *
from ...utilities.validator import vld_role, vld_invitation
from ...utilities.utils import random_number, saving_image, split_date_time,random_string_number
from ..Template.models import TemplateModels
from ..Category.models import CategoryModels

from flask import request, current_app as app
from werkzeug.utils import secure_filename
from datetime import datetime
from twilio.rest import Client

import time, json


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
            
            requiredData = ["category_id", "template_id", "title", "personal_data", "inv_setting"]
            for req in requiredData:
                if req not in datas:
                    return parameter_error(f"Missing {req} in Request Body.")
            # Checking Request Body ---------------------------------------- Finish

            # Initialize Request Data ---------------------------------------- Start
            categoryId = datas["category_id"]
            templateId = datas["template_id"]
            title = datas["title"].strip()
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
            # wallpaperFileName = ""
            # if wallpaper != "":
            #     wallpaperFileName = secure_filename(time.strftime("%Y-%m-%d %H:%M:%S")+"_"+invCode+"_wallpaper.jpg")
            #     wallpaperPath = os.path.join(app.config['USER_INVITATION_FILE'], wallpaperFileName)
            #     saving_image(wallpaper, wallpaperPath)
            # Saving File ---------------------------------------- Finish

            # Insert Data ---------------------------------------- Start
            timestamp = int(round(time.time()*1000))
            titlelink = title.replace(' ', '-')
            invLink =  app.config['FE_URL']+"/"+invCode+"/"+titlelink
            personalData = json.dumps(personalData)
            invSett = json.dumps(invSett)
            query = INV_ADD_QUERY
            values = (accLevel, user_id, categoryId, templateId, title, personalData, invSett, invCode, invLink, timestamp, user_id, timestamp, user_id)
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
            
            # Get Data Template ---------------------------------------- Start
            query = TMPLT_GET_ALL_QUERY
            template = DBHelper().execute(query)
            if len(template) < 1:
                return not_found("Data template tidak dapat ditemukan.")
            # Get Data Template ---------------------------------------- Finish

            # Join Data ---------------------------------------- Start
            # Category
            for invitation in result:
                for category in resultCtgr:
                    if invitation["category_id"] == category["id"]:
                        invitation["category"] = category["category"]

            # Template
            for invitation in result:
                for temp in template:
                    if invitation["template_id"] == temp["id"]:
                        invitation["template_title"] = temp["title"]
                        invitation["template_thumb"] = temp["thumbnail"]
            # Join Data ---------------------------------------- Finish

            # Generate File URL ---------------------------------------- Start
            if len(result) >= 1:
                detailRequestURL = str(request.url).find('?')
                if detailRequestURL != -1:
                    index = detailRequestURL
                    request.url = request.url[:index]
            for item in result:
                # item["wallpaper"] = f"{request.url_root}invitation/media/{item['wallpaper']}"
                item["template_thumb"] = f"{request.url_root}template/media/thumbnail/{item['template_thumb']}"
            # Generate File URL ---------------------------------------- Finish
            
            # Response Data ---------------------------------------- Start
            query1 = GUEST_GET_BY_CODE_QUERY
            query2 = GRTG_GET_BY_CODE_QUERY
            response = []
            for rsl in result:
                values = (rsl['code'], )
                guest = DBHelper().get_count_filter_data(query1, values)
                greeting = DBHelper().get_count_filter_data(query2, values)
                createdAt = split_date_time(datetime.fromtimestamp(rsl['created_at']/1000))
                updatedAt = split_date_time(datetime.fromtimestamp(rsl['updated_at']/1000))
                data = {
                    "invitation_id" : rsl["id"],
                    "user_id" : rsl["user_id"],
                    "category_id" : rsl["category_id"],
                    "category" : rsl["category"],
                    "template_id" : rsl["template_id"],
                    "invitation_title" : rsl["title"].title(),
                    "personal_data" : json.loads(rsl["personal_data"]),
                    "invitation_code" : rsl["code"],
                    "invitation_link" : rsl["link"],
                    "template_thumb" : rsl["template_thumb"],
                    "guest_count" : guest,
                    "greeting_count" : greeting,
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
            access = vld_role(user_role)
            if not access:
                return authorization_error()
            # Access Validation ---------------------------------------- Finish
            
            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            requiredData = ["invitation_id", "title", "personal_data", "inv_setting"]
            for req in requiredData:
                if req not in datas:
                    return parameter_error(f"Missing {req} in Request Body.")
            # Checking Request Body ---------------------------------------- Finish

            # Initialize Request Data ---------------------------------------- Start
            invId = datas["invitation_id"]
            title = datas["title"]
            personalData = datas["personal_data"]
            invSett = datas["inv_setting"]
            # Initialize Request Data ---------------------------------------- Finish
            
            # Data Validation ---------------------------------------- Start
            query = INV_GET_BY_ID_QUERY
            values = (invId,)
            result = DBHelper().get_data(query, values)
            if len(result) < 1 :
                return not_found("Data undangan tidak dapat ditemukan.")
            
            # ctgrCheck = vld_invitation(ctgr)
            # if len(ctgrCheck) != 0:
                return defined_error(ctgrCheck, "Bad Request", 400)
            # Data Validation ---------------------------------------- Finish
            
            # Update Data ---------------------------------------- Start
            timestamp = int(round(time.time()*1000))
            # query = CTGR_UPDATE_QUERY
            # values = (ctgr, timestamp, user_id, ctgrId)
            # DBHelper().save_data(query, values)
            # Update Data ---------------------------------------- Finish

            # Log Activity Record ---------------------------------------- Start
            activity = f"Admin dengan id {user_id} mengubah kategori {result[0]['category']} menjadi {ctgr}"
            query = LOG_ADD_QUERY
            values = (user_id, activity, )
            # DBHelper().save_data(query, values)
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
            access = vld_role(user_role)
            if access: # Access = True -> Admin
                return authorization_error()
            # Access Validation ---------------------------------------- Finish

            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            if "invitation_id" not in datas:
                return parameter_error(f"Missing 'category_id' in Request Body")
            
            invId = datas["invitation_id"]
            if invId == "":
                return defined_error("Id undangan tidak boleh kosong", "Defined Error", 400)
            # Checking Request Body ---------------------------------------- Finish
            
            # Checking Data Invitation ---------------------------------------- Start
            query = INV_GET_BY_ID_QUERY
            values = (invId,)
            result = DBHelper().get_data(query, values)
            if len(result) < 1 :
                return not_found(f"Data undangan dengan Id {invId} tidak dapat ditemukan.")
            # Checking Data Invitation ---------------------------------------- Finish

            # Get Data Category ---------------------------------------- Start
            invitation = result[0]
            query = CTGR_GET_BY_ID_QUERY
            values = (invitation['category_id'], )
            category = DBHelper().get_data(query, values)
            if len(category) < 1 :
                return not_found(f"Data kategori dengan Id {invitation['category_id']} tidak dapat ditemukan.")
            # Get Data Category ---------------------------------------- Finish

            # Get Data Template ---------------------------------------- Start
            query = TMPLT_GET_BY_ID_QUERY
            values = (invitation['template_id'], )
            templates = DBHelper().get_data(query, values)
            if len(templates) < 1 :
                return not_found(f"Data template dengan Id {invitation['template_id']} tidak dapat ditemukan.")
            # Get Data Template ---------------------------------------- Finish
            
            # Generate Invitation File URL ---------------------------------------- Start
            if len(result) >= 1:
                detailRequestURL = str(request.url).find('?')
                if detailRequestURL != -1:
                    index = detailRequestURL
                    request.url = request.url[:index]
            
            invitation["category"] = category[0]["category"]
            invitation["template_title"] = templates[0]["title"]
            invitation["temp_thumb"] = f"{request.url_root}template/media/thumbnail/{templates[0]['thumbnail']}"
            invitation["temp_css"] = f"{request.url_root}template/media/css/{templates[0]['css_file']}"
            invitation["temp_js"] = f"{request.url_root}template/media/js/{templates[0]['js_file']}"
            invitation["temp_wall"] = f"{request.url_root}template/media/wallpaper/{templates[0]['wallpaper']}"
            # Generate Invitation File URL ---------------------------------------- Finish
            
            # Response Data ---------------------------------------- Start
            invitation["personal_data"] = json.loads(invitation["personal_data"])
            invitation["inv_setting"] = json.loads(invitation["inv_setting"])
            invitation["created_at"] = split_date_time(datetime.fromtimestamp(invitation["created_at"]/1000))
            invitation["updated_at"] = split_date_time(datetime.fromtimestamp(invitation["updated_at"]/1000))
            response = {
                    "invitation_id" : invitation["id"],
                    "user_id" : invitation["user_id"],
                    "category_id" : invitation["category_id"],
                    "category" : invitation["category"],
                    "invitation_title" : invitation["title"].title(),
                    "personal_data" : invitation["personal_data"],
                    "invitation_code" : invitation["code"],
                    "invitation_link" : invitation["link"],
                    "created_at": invitation["created_at"],
                    "updated_at" : invitation["updated_at"],
                    "template_id" : invitation["template_id"],
                    "template_thumb" : invitation["temp_thumb"],
                    "template_css" : invitation["temp_css"],
                    "template_js" : invitation["temp_js"],
                    "template_wall" : invitation["temp_wall"],
                    "template_title" : invitation["template_title"]
            }
            # Response Data ---------------------------------------- Finish

            # Return Response ======================================== 
            return success_data(response)
        
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

    # SHARE INVITATION ============================================================ Begin
    # 
    def share_invitation(datas):
        try:
            # Access Validation ---------------------------------------- Start
            # accLevel = 2  # 1 = Admin | 2 = User
            # access = vld_role(user_role)
            # if access: # Access = True -> Admin
            #     return authorization_error()
            # Access Validation ---------------------------------------- Finish

            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            requiredData = ["to", "message"]
            for req in requiredData:
                if req not in datas:
                    return parameter_error(f"Missing {req} in Request Body.")
            # Checking Request Body ---------------------------------------- Finish

            # Initialize Request Data ---------------------------------------- Start
            to = datas["to"]
            message = datas["message"]
            # Initialize Request Data ---------------------------------------- Finish
            
            # Data Validation ---------------------------------------- Start
            account_sid = app.config['ACCOUNT_SID']
            auth_token = app.config['AUTH_TOKEN']
            client = Client(account_sid, auth_token)

            message = client.messages.create(
            from_='whatsapp:+6283861367245',
            body=f'{message}',
            to=f'whatsapp:{to}'
            )

            print(message.sid)
            # Data Validation ---------------------------------------- Finish

            # Insert Data ---------------------------------------- Start
            # Insert Data ---------------------------------------- Finish

            # Log Activity Record ---------------------------------------- Start
            # Log Activity Record ---------------------------------------- Finish

            # Return Response ======================================== 
            return success_data(message.sid)
        
        except Exception as e:
            return bad_request(str(e))
    # SHARE INVITATION ============================================================ End
# CATEGORY MODEL CLASS ============================================================ End