from ...utilities.responseHelper import *
from ...utilities.dbHelper import DBHelper
from ...utilities.queries import *
from ...utilities.validator import vld_role, vld_request_template
from ...utilities.utils import random_number, saving_image, saving_file, split_date_time
from ..Category.models import CategoryModels

from flask import request, current_app as app
from werkzeug.utils import secure_filename
from datetime import datetime

import time, os
  
# REQUEST TEMPLATE MODEL CLASS ============================================================ Begin
class ReqTemplateModels():
    # CREATE REQUEST TEMPLATE ============================================================ Begin
    # Clear// input data checker belum
    def add_request_template(user_id, user_role, datas):
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
            types = datas["type"]
            catgId = datas["category_id"]
            # Initialize Data Input ---------------------------------------- Finish

            # Data Validation ---------------------------------------- Start
            reqTemCheck = vld_request_template(tempDesign, deadline, catgId)
            if len(reqTemCheck) != 0:
                return defined_error(reqTemCheck, "Bad Request", 400)
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
            values = (user_id, acclevel, catgId, designFileName, descript, deadline, types, status, timestamp, user_id, timestamp, user_id)
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
    # CREATE REQUEST TEMPLATE ============================================================ End

    # GET ALL REQUEST TEMPLATE ============================================================ Begin
    def view_request_template(user_id, user_role):
        try:
            # Set Access Level ---------------------------------------- Start
            access = vld_role(user_role)
            # Set Access Level ---------------------------------------- Finish

            # Get & Check Data ---------------------------------------- Start
            if access:
                query = REQ_GET_ALL_QUERY
                values = (2, )
            else:
                query = REQ_GET_BY_USER_QUERY
                values = (user_id, 2, )
            result = DBHelper().get_data(query, values)
            if len(result) < 1:
                return not_found("Data request tidak dapat ditemukan.")
            # Get & Check Data ---------------------------------------- Finish
            
            # Get & Check Data ---------------------------------------- Start
            if access:
                query = PROF_USER_GET_QUERY
                values = (2, )
            else:
                query = PROF_GET_BY_ID_QUERY
                values = (user_id, 2, )
            profiles = DBHelper().get_data(query, values)
            if len(profiles) < 1:
                return not_found("Data profile tidak dapat ditemukan.")
            # Get & Check Data ---------------------------------------- Finish
            
            # Get Data Category ---------------------------------------- Start
            query = CTGR_GET_ALL_QUERY
            category = DBHelper().execute(query)
            if len(category) < 1:
                return not_found("Data kategori tidak dapat ditemukan.")
            # Get Data Category ---------------------------------------- Finish

            # Join Data ---------------------------------------- Start
            for req in result:
                for ctg in category:
                    if req["category"] == ctg["id"]:
                        req["category_id"] = ctg["id"]
                        req["category"] = ctg["category"]
                for prof in profiles:
                    if req["user_id"] == prof["user_id"]:
                        req["fullname"] = prof["first_name"]+" "+prof["middle_name"]+" "+prof["last_name"]
            # Join Data ---------------------------------------- Finish

            # Generate File URL ---------------------------------------- Start
            if len(result) >= 1:
                detailRequestURL = str(request.url).find('?')
                if detailRequestURL != -1:
                    index = detailRequestURL
                    request.url = request.url[:index]
            for rsl in result:
                rsl['design_file'] = f"{request.url_root}template/request/media/{rsl['design_file']}"
                if int(rsl["type"]) == 0:
                    rsl["type_txt"] = "Private"
                elif int(rsl["type"]) == 1:
                    rsl["type_txt"] = "Public"
                
                if rsl['status'] == 0:
                    rsl['status_txt'] = "Menunggu"
                elif rsl['status'] == 1:
                    rsl['status_txt'] = "Disetujui"
                elif rsl['status'] == 2:
                    rsl['status_txt'] = "Dalam Proses"
                elif rsl['status'] == 3:
                    rsl['status_txt'] = "Ditolak"
                elif rsl['status'] == 4:
                    rsl['status_txt'] = "Selesai"
                # 0 = waiting | 1 = acc | 2 = proccess | 3 = decline | 4 = clear

                if rsl['type'] == 0:
                    rsl['type'] = "Private"
                elif rsl['type'] == 1:
                    rsl['type'] = "Public"
                
            # Generate File URL ---------------------------------------- Finish

            # Response Data ---------------------------------------- Start
            response = []
            for rsl in result:
                createdAt = split_date_time(datetime.fromtimestamp(rsl['created_at']/1000))
                updatedAt = split_date_time(datetime.fromtimestamp(rsl['updated_at']/1000))
                data = {
                    "req_id" : rsl["id"],
                    "user_id" : rsl["user_id"],
                    "fullname" : rsl["fullname"],
                    "user_level" : rsl["user_level"],
                    "category" : rsl["category"],
                    "deadline" : rsl["deadline"],
                    "status" : rsl["status"],
                    "status_txt" : rsl["status_txt"],
                    "type": rsl["type"],
                    "type_txt": rsl["type_txt"],
                    "description": rsl["description"],
                    "design_file": rsl['design_file'],
                    "created_at" : createdAt,
                    "updated_at" : updatedAt
                }
                response.append(data)
            # Response Data ---------------------------------------- Finish

            # Return Response ======================================== 
            return success_data(response)
        
        except Exception as e:
            return bad_request(str(e))
    # GET ALL REQUEST TEMPLATE ============================================================ End

    # # UPDATE GUEST ============================================================ Begin
    # # 
    # def edit_guest(user_id, user_role, datas):
    #     try:
    #         # Access Validation ---------------------------------------- Start
    #         access = vld_role(user_role)
    #         accLevel = 2
    #         # Access Validation ---------------------------------------- Finish

    #         # Checking Request Body ---------------------------------------- Start
    #         if datas == None:
    #             return invalid_params()
            
    #         requiredData = ["guest_id", "invitation_code", "name", "address", "phone"]
    #         for req in requiredData:
    #             if req not in datas:
    #                 return parameter_error(f"Missing {req} in Request Body")
    #         # Checking Request Body ---------------------------------------- Finish
            
    #         # Inisialize Data Input ---------------------------------------- Start
    #         gueId = datas["guest_id"]
    #         invCode = datas["invitation_code"]
    #         name = datas["name"]
    #         address = datas["address"]
    #         phone = datas["phone"]
    #         # Inisialize Data Input ---------------------------------------- Finish
            
    #         # Data Validation ---------------------------------------- Start
    #         query = GUEST_GET_BY_ID_QUERY
    #         values = (gueId, )
    #         result = DBHelper().get_data(query, values)
    #         if len(result) < 1 :
    #             return not_found("Data tamu tidak dapat ditemukan.")
            
    #         guestCheck, phone = vld_guest(name, address, phone, invCode, False)
    #         if len(guestCheck) != 0:
    #             return defined_error(guestCheck, "Bad Request", 400)
    #         # Data Validation ---------------------------------------- Finish
            
    #         # Update Data ---------------------------------------- Start
    #         timestamp = int(round(time.time()*1000))
    #         query = GUEST_UPDATE_QUERY
    #         values = (name, address, phone, timestamp, user_id, gueId, )
    #         DBHelper().save_data(query, values)
    #         # Update Data ---------------------------------------- Finish

    #         # Log Activity Record ---------------------------------------- Start
    #         activity = f"{user_role.title()} dengan id {user_id} mengubah data tamu {result[0]['name']}."
    #         query = LOG_ADD_QUERY
    #         values = (user_id, accLevel, activity, timestamp, )
    #         DBHelper().save_data(query, values)
    #         # Log Activity Record ---------------------------------------- Finish

    #         # Return Response ======================================== 
    #         return success(message="Updated!")
            
    #     except Exception as e:
    #         return bad_request(str(e))
    # # UPDATE GUEST ============================================================ End

    # DELETE GUEST ============================================================ Begin
    # 
    def delete_guest(user_id, user_role, datas):     
        try:
            # Set Access Level ---------------------------------------- Start
            access = vld_role(user_role)
            accLevel = 1 if access else 2
            # Set Access Level ---------------------------------------- Finish

            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            if "request_id" not in datas:
                return parameter_error("Missing 'request_id' in Request Body.")
            
            reqId = datas["request_id"]
            if reqId == "":
                return defined_error("Id tamu tidak boleh kosong.", "Defined Error", 400)
            # Checking Request Body ---------------------------------------- Finish
            
            # Data Validation ---------------------------------------- Start
            query = REQ_GET_BY_ID_QUERY
            values = (reqId,)
            result = DBHelper().get_data(query, values)
            if len(result) < 1 :
                return not_found("Data tamu tidak dapat ditemukan.")
            # Data Validation ---------------------------------------- Finish

            # Delete Data ---------------------------------------- Start
            timestamp = int(round(time.time()*1000))
            query = REQ_DELETE_QUERY
            values = (timestamp, user_id, reqId)
            DBHelper().save_data(query, values)
            # Delete Data ---------------------------------------- Finish

            # Log Activity Record ---------------------------------------- Start
            activity = f"{user_role.title()} dengan id {user_id} menghapus data request {result[0]['id']}."
            query = LOG_ADD_QUERY
            values = (user_id, accLevel, activity, timestamp, )
            DBHelper().save_data(query, values)
            # Log Activity Record ---------------------------------------- Finish

            # Return Response ======================================== 
            return success(message="Deleted!")
            
        except Exception as e:
            return bad_request(str(e))
    # DELETE GUEST ============================================================ End
    
    # GET ALL REQUEST TEMPLATE ============================================================ Begin
    def view_detail_request_template(user_id, user_role, datas):
        try:
            # Set Access Level ---------------------------------------- Start
            access = vld_role(user_role)
            # Set Access Level ---------------------------------------- Finish

            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            if "request_id" not in datas:
                return parameter_error("Missing 'request_id' in Request Body.")
            
            reqId = datas["request_id"]
            if reqId == "":
                return defined_error("Id request tidak boleh kosong.", "Defined Error", 400)
            # Checking Request Body ---------------------------------------- Finish

            # Get & Check Data ---------------------------------------- Start
            query = REQ_GET_BY_ID_QUERY
            values = (reqId, )
            result = DBHelper().get_data(query, values)
            if len(result) < 1:
                return not_found("Data request tidak dapat ditemukan.")
            # Get & Check Data ---------------------------------------- Finish
            print(result)
            
            # Get & Check Data ---------------------------------------- Start
            query = PROF_GET_BY_ID_QUERY
            values = (result[0]['user_id'], 2, )
            profiles = DBHelper().get_data(query, values)
            if len(profiles) < 1:
                return not_found("Data profile tidak dapat ditemukan.")
            # Get & Check Data ---------------------------------------- Finish
            
            # Get Data Category ---------------------------------------- Start
            query = CTGR_GET_BY_ID_QUERY
            values = (result[0]['category'],)
            category = DBHelper().get_data(query, values)
            if len(category) < 1:
                return not_found("Data kategori tidak dapat ditemukan.")
            # Get Data Category ---------------------------------------- Finish

            # Join Data ---------------------------------------- Start
            for req in result:
                for ctg in category:
                    if req["category"] == ctg["id"]:
                        req["category_id"] = ctg["id"]
                        req["category"] = ctg["category"]
                for prof in profiles:
                    if req["user_id"] == prof["user_id"]:
                        req["fullname"] = prof["first_name"]+" "+prof["middle_name"]+" "+prof["last_name"]
            # Join Data ---------------------------------------- Finish

            # Generate File URL ---------------------------------------- Start
            if len(result) >= 1:
                detailRequestURL = str(request.url).find('?')
                if detailRequestURL != -1:
                    index = detailRequestURL
                    request.url = request.url[:index]
            for rsl in result:
                rsl['design_file'] = f"{request.url_root}template/request/media/{rsl['design_file']}"
                if int(rsl["type"]) == 0:
                    rsl["type_txt"] = "Privasi"
                elif int(rsl["type"]) == 1:
                    rsl["type_txt"] = "Publik"
                
                if rsl['status'] == 0:
                    rsl['status_txt'] = "Menunggu"
                elif rsl['status'] == 1:
                    rsl['status_txt'] = "Disetujui"
                elif rsl['status'] == 2:
                    rsl['status_txt'] = "Dalam Proses"
                elif rsl['status'] == 3:
                    rsl['status_txt'] = "Ditolak"
                elif rsl['status'] == 4:
                    rsl['status_txt'] = "Selesai"
                # 0 = waiting | 1 = acc | 2 = proccess | 3 = decline | 4 = clear

                if rsl['type'] == 0:
                    rsl['type'] = "Private"
                elif rsl['type'] == 1:
                    rsl['type'] = "Public"
            # Generate File URL ---------------------------------------- Finish

            # Response Data ---------------------------------------- Start
            result = result[0]
            createdAt = split_date_time(datetime.fromtimestamp(result['created_at']/1000))
            updatedAt = split_date_time(datetime.fromtimestamp(result['updated_at']/1000))
            response = {
                "req_id" : result["id"],
                "user_id" : result["user_id"],
                "fullname" : result["fullname"],
                "user_level" : result["user_level"],
                "category" : result["category"],
                "deadline" : result["deadline"],
                "status" : result["status"],
                "status_txt" : result["status_txt"],
                "type": result["type"],
                "type_txt": result["type_txt"],
                "description": result["description"],
                "design_file": result['design_file'],
                "created_at" : createdAt,
                "updated_at" : updatedAt
            }
            # Response Data ---------------------------------------- Finish

            # Return Response ======================================== 
            return success_data(response)
        
        except Exception as e:
            return bad_request(str(e))
    # GET ALL REQUEST TEMPLATE ============================================================ End
# REQUEST TEMPLATE MODEL CLASS ============================================================ End
