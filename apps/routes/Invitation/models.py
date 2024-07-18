from ...utilities.responseHelper import *
from ...utilities.dbHelper import DBHelper
from ...utilities.queries import *
from ...utilities.validator import vld_role, vld_invitation
from ...utilities.utils import random_number, saving_image, split_date_time, random_string_number

from flask import request, current_app as app
from werkzeug.utils import secure_filename
from datetime import datetime
from twilio.rest import Client

import time, json,os


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
            print(personalData['galeri_photo'])
            
            # Saving File ---------------------------------------- Start
            # wallpaper
            wpFileName = ""
            # if len(personalData) > 0
            if personalData['womans_photo'] != "":
                wpFileName = secure_filename(time.strftime("%Y-%m-%d %H:%M:%S")+"_"+invCode+"_woman_photo_"+user_id+".jpg")
                wpPath = os.path.join(app.config['USER_INVITATION_FILE'], wpFileName)
                saving_image(personalData['womans_photo'], wpPath)
                personalData['womans_photo'] = wpFileName
            if personalData['mans_photo'] != "":
                mpFileName = secure_filename(time.strftime("%Y-%m-%d %H:%M:%S")+"_"+invCode+"_man_photo_"+user_id+".jpg")
                mpPath = os.path.join(app.config['USER_INVITATION_FILE'], mpFileName)
                saving_image(personalData['mans_photo'], mpPath)
                personalData['mans_photo'] = mpFileName
            if personalData['galeri_photo'] != "":
                gpFileName = secure_filename(time.strftime("%Y-%m-%d %H:%M:%S")+"_"+invCode+"_gallery_"+user_id+".jpg")
                gpPath = os.path.join(app.config['GALLERY_INVITATION_FILE'], gpFileName)
                saving_image(personalData['galeri_photo'], gpPath)
                personalData['galeri_photo'] = gpFileName
            # Saving File ---------------------------------------- Finish

            # Insert Data ---------------------------------------- Start
            timestamp = int(round(time.time()*1000))
            titlelink = title.replace(' ', '-')
            invLink =  titlelink
            personalData = json.dumps(personalData)
            invSett = json.dumps(invSett)
            query = INV_ADD_QUERY
            values = (accLevel, user_id, categoryId, templateId, title, personalData, invSett, invCode, invLink, timestamp, user_id, timestamp, user_id)
            resReturn = DBHelper().save_return(query, values)
            # Insert Data ---------------------------------------- Finish

            # Log Activity Record ---------------------------------------- Start
            activity = f"User dengan id {user_id} telah membuat undangan baru: {title}."
            query = LOG_ADD_QUERY
            values = (user_id, accLevel, activity, timestamp, )
            # DBHelper().save_data(query, values)
            # Log Activity Record ---------------------------------------- Finish
            
            # Response Data ---------------------------------------- Start
            response = {
                "inv_id": resReturn,
                "inv_code": invCode
            }
            # Response Data ---------------------------------------- Finish

            # Return Response ======================================== 
            return success_data(response, statusCode=201)
        
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
            query = INV_GET_BY_USR_QUERY
            values = (user_id, accLevel, )
            result = DBHelper().get_data(query, values)
            if len(result) < 1:
                return not_found("Data undangan tidak dapat ditemukan.")
            # Checking Data ---------------------------------------- Finish
            
            # Get Data Category ---------------------------------------- Start
            query = CTGR_GET_ALL_QUERY
            resultCtgr = DBHelper().execute(query)
            if len(resultCtgr) < 1:
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
    # Clear
    def edit_invitation(user_id, user_role, datas):
        try:
            # Access Validation ---------------------------------------- Start
            access = vld_role(user_role)
            accLevel = 1 if access else 2
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
                return not_found(f"Data undangan dengan id {invId} tidak dapat ditemukan.")
            
            # Data Validation ---------------------------------------- Finish
            
            # Data Validation ---------------------------------------- Start
            invCheck, personalData, invCode = vld_invitation(result[0]["category_id"], result[0]["template_id"], title, personalData, False)
            if len(invCheck) != 0:
                return defined_error(invCheck, "Bad Request", 400)
            # Data Validation ---------------------------------------- Finish
            
            # Update Data ---------------------------------------- Start
            timestamp = int(round(time.time()*1000))
            personalData = json.dumps(personalData)
            invSett = json.dumps(invSett)
            query = INV_UPDATE_QUERY
            values = (title, personalData, invSett, timestamp, user_id, invId)
            DBHelper().save_data(query, values)
            # Update Data ---------------------------------------- Finish

            # Log Activity Record ---------------------------------------- Start
            activity = f"{user_role.title()} dengan id {user_id} mengubah data undangan {result[0]['title']}."
            query = LOG_ADD_QUERY
            values = (user_id, accLevel, activity, timestamp, )
            DBHelper().save_data(query, values)
            # Log Activity Record ---------------------------------------- Finish

            # Return Response ======================================== 
            return success(message="Updated!")
            
        except Exception as e:
            return bad_request(str(e))
    # UPDATE INVITATION ============================================================ End

    # DELETE INVITATION ============================================================ Begin
    # Clear
    def delete_invitation(user_id, user_role, datas):
        try:
            # Access Validation ---------------------------------------- Start
            access = vld_role(user_role)
            accLevel = 1 if access else 2
            # Access Validation ---------------------------------------- Finish

            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            if "invitation_id" not in datas:
                return parameter_error(f"Missing 'invitation_id' in Request Body.")
            
            invId = datas["invitation_id"]
            if invId == "":
                return defined_error("Id undangan tidak boleh kosong", "Defined Error", 400)
            # Checking Request Body ---------------------------------------- Finish
            
            # Checking Data ---------------------------------------- Finish
            query = INV_GET_BY_ID_QUERY
            values = (invId,)
            result = DBHelper().get_data(query, values)
            if len(result) < 1 :
                return not_found(f"Data undangan dengan id {invId} tidak dapat ditemukan.")
            # Checking Data ---------------------------------------- Finish
            
            # Delete Data ---------------------------------------- Start
            timestamp = int(round(time.time()*1000))
            query = INV_DELETE_QUERY
            values = (timestamp, user_id, invId, )
            DBHelper().save_data(query, values)
            # Delete Data ---------------------------------------- Finish

            # Delete Join Data ---------------------------------------- Start
            invCode = result[0]['code']
            # Guest
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
            activity = f"{user_role.title()} dengan id {user_id} menghapus data undangan {invId}."
            query = LOG_ADD_QUERY
            values = (user_id, accLevel, activity, timestamp, )
            DBHelper().save_data(query, values)
            # Log Activity Record ---------------------------------------- Finish

            # Return Response ======================================== 
            return success(message="Deleted!")
            
        except Exception as e:
            return bad_request(str(e))
    # DELETE INVITATION ============================================================ End

    # GET DETAIL INVITATION ============================================================ Begin
    # Clear // sesuaikan kategori
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
            invitation["temp_wall2"] = f"{request.url_root}template/media/wallpaper/{templates[0]['wallpaper_2']}"
            # Generate Invitation File URL ---------------------------------------- Finish
            
            # Set Data ---------------------------------------- Start
            invitation["personal_data"] = json.loads(invitation["personal_data"])
            invitation["inv_setting"] = json.loads(invitation["inv_setting"])
            invitation["created_at"] = split_date_time(datetime.fromtimestamp(invitation["created_at"]/1000))
            invitation["updated_at"] = split_date_time(datetime.fromtimestamp(invitation["updated_at"]/1000))
            if invitation["category"].upper() == "PERNIKAHAN":
                for data in invitation["personal_data"]:
                    if data.upper() == "MARRIAGE":
                        invitation["personal_data"][data] = split_date_time(datetime.fromtimestamp(invitation["personal_data"][data]/1000))
                    if data.upper() == "RECEPTION":
                        invitation["personal_data"][data] = split_date_time(datetime.fromtimestamp(invitation["personal_data"][data]/1000))
                    if data.upper() == "WOMANS_PHOTO":
                        invitation["personal_data"][data] = f"{request.url_root}invitation/media/{invitation['personal_data'][data]}"
                    if data.upper() == "MANS_PHOTO":
                        invitation["personal_data"][data] = f"{request.url_root}invitation/media/{invitation['personal_data'][data]}"
            # Set Data ---------------------------------------- Finish

            # Response Data ---------------------------------------- Start
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
                    "template_wall2" : invitation["temp_wall2"],
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