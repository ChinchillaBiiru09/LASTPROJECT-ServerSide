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
    # CREATE REQUEST TEMPLATE ============================================================ End

    # GET ALL REQUEST TEMPLATE ============================================================ Begin
    def view_request_template(user_id):
        try:
            print("hmm")
            # Get & Check Data ---------------------------------------- Start
            query = REQ_GET_BY_USER_QUERY
            values = (user_id, 2, )
            result = DBHelper().get_data(query, values)
            if len(result) < 1:
                return not_found("Data request tidak dapat ditemukan.")
            # Get & Check Data ---------------------------------------- Finish
            print(result)
            
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
            # Join Data ---------------------------------------- Finish

            # Generate File URL ---------------------------------------- Start
            if len(result) >= 1:
                detailRequestURL = str(request.url).find('?')
                if detailRequestURL != -1:
                    index = detailRequestURL
                    request.url = request.url[:index]
            for rsl in result:
                rsl['design_file'] = f"{request.url_root}template/request/media/{rsl['design_file']}"
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
                    # "user_name" : rsl["user_name"],
                    "user_level" : rsl["user_level"],
                    "category" : rsl["category"],
                    "deadline" : rsl["deadline"],
                    "status" : rsl["status"],
                    "status_txt" : rsl["status_txt"],
                    "type": rsl["type"],
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
# REQUEST TEMPLATE MODEL CLASS ============================================================ End
