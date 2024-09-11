from ...utilities.responseHelper import *
from ...utilities.dbHelper import DBHelper
from ...utilities.queries import *
from ...utilities.validator import vld_guest, vld_role
from ...utilities.utils import split_date_time

from flask import request, current_app as app
from datetime import datetime
from io import BytesIO
from werkzeug.utils import secure_filename
import time, json, base64, os, pandas as pd

# GUEST MODEL CLASS ============================================================ Begin
class GuestModels():
    # CREATE GUEST ============================================================ Begin
    # Clear
    def add_guest(user_id, user_role, datas):
        try:
            # Set Access Level ---------------------------------------- Start
            access = vld_role(user_role)
            accLevel = 2
            if access: # Access = True -> Admin
                return authorization_error()
            # Set Access Level ---------------------------------------- Finish
            
            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            requiredData = ["invitation_code", "name", "address", "phone"]
            for req in requiredData:
                if req not in datas:
                    return parameter_error(f"Missing {req} in Request Body")
            # Checking Request Body ---------------------------------------- Finish
            
            # Intialize ---------------------------------------- Start
            invCode = datas["invitation_code"]
            name = datas["name"]
            address = datas["address"]
            phone = datas["phone"]
            # Intialize ---------------------------------------- Finish

            # Data Validation ---------------------------------------- Start
            checkResult, phone = vld_guest(name, address, phone, invCode)
            if len(checkResult) != 0:
                return defined_error(checkResult, "Bad Request", 400)
            # Data Validation ---------------------------------------- Finish

            # Get Invitation Data ---------------------------------------- Start
            query = INV_CHK_CODE_QUERY
            values = (invCode,)
            result = DBHelper().get_data(query, values)
            if len(result) < 1:
                return not_found(f"Data undangan dengan kode {invCode} tidak dapat ditemukan.")
            inv = result[0]
            # Get Invitation Data ---------------------------------------- End

            # Get Category Data ---------------------------------------- Start
            query = CTGR_GET_ALL_QUERY
            categories = DBHelper().execute(query)
            for category in categories:
                if category['id'] == inv['category_id']:
                    inv['category'] = category['category']
            # Get Category Data ---------------------------------------- End
            
            # Validation Data ---------------------------------------- Start
            inv['detail_info'] = json.loads(inv['detail_info'])
            match inv['category'].upper():
                case "PERNIKAHAN":
                    expiredEvent = datetime.fromtimestamp(inv['detail_info']['reception_end']/1000)
                case "ULANG TAHUN":
                    expiredEvent = datetime.fromtimestamp(inv['detail_info']['end']/1000)
                case "GRADUATION PARTY":
                    expiredEvent = datetime.fromtimestamp(inv['detail_info']['end']/1000)
                case _:
                    expiredEvent = 0
                    print("Kategori tidak dikenali")
            # Validation Data ---------------------------------------- Finish
            
            # Insert Data ---------------------------------------- Start
            now = datetime.now()
            timestamp = int(round(time.time()*1000))
            if expiredEvent > now:
                query = GUEST_ADD_QUERY
                values = (user_id, accLevel, inv['category_id'], invCode, name, address, phone, timestamp, user_id, timestamp, user_id)
                DBHelper().save_data(query, values)
            else:
                return bad_request("Data tamu gagal ditambahkan karena acara telah berakhir.")
            # Insert Data ---------------------------------------- Finish

            # Log Activity Record ---------------------------------------- Start
            activity = f"User dengan id {user_id} menambahkan data tamu baru: {name}."
            query = LOG_ADD_QUERY
            values = (user_id, accLevel, activity, timestamp, )
            DBHelper().save_data(query, values)
            # Log Activity Record ---------------------------------------- Finish

            # Return Response ======================================== 
            return success(statusCode=201)
        
        except Exception as e:
            return bad_request(str(e))
    # CREATE GUEST ============================================================ End

    # DUPLICATE GUEST ============================================================ Begin
    # Clear
    def copy_paste_guest(user_id, user_role, user_name, datas):   
        try:
            # Set Access Level ---------------------------------------- Start
            access = vld_role(user_role)
            accLevel = 2
            if access: # Access = True -> Admin
                return authorization_error()
            # Set Access Level ---------------------------------------- Finish

            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            requiredData = ["invitation_code", "reference_code"]
            for req in requiredData:
                if req not in datas:
                    return parameter_error(f"Missing {req} in Request Body")
            # Checking Request Body ---------------------------------------- Finish

            # Initialize Data Input ---------------------------------------- Finish
            invCode = datas['invitation_code']
            refCode = datas['reference_code']
            # Initialize Data Input ---------------------------------------- Finish

            # Checking Data ---------------------------------------- Start
            query = INV_CHK_CODE_QUERY
            values = (invCode,)
            result = DBHelper().get_data(query, values)
            if len(result) < 1:
                return not_found(f"Data undangan dengan kode {invCode} tidak dapat ditemukan.")
            result = result[0]
            # Checking Data ---------------------------------------- End

            # Get Invitation Data ---------------------------------------- Start
            query = INV_CHK_CODE_QUERY
            values = (refCode,)
            invitations = DBHelper().get_data(query, values)
            if len(invitations) < 1:
                return not_found(f"Data undangan dengan kode {refCode} tidak dapat ditemukan.")
            invitation = invitations[0]
            # Get Invitation Data ---------------------------------------- End
            
            # Get Category Data ---------------------------------------- Start
            query = CTGR_GET_ALL_QUERY
            categories = DBHelper().execute(query)
            for category in categories:
                if category['id'] == result['category_id']:
                    result['category'] = category['category']
            # Get Category Data ---------------------------------------- End
            
            # Get Guest Data ---------------------------------------- Start
            query = GUEST_GET_BY_CODE_QUERY
            values = (refCode, )
            guests = DBHelper().get_data(query, values)
            if len(guests) < 1:
                return not_found(f"Data tamu dari undangan {invitation['title']} tidak dapat ditemukan.")
            # Get Guest Data ---------------------------------------- Finish

            # Validation Data ---------------------------------------- Start
            result['detail_info'] = json.loads(result['detail_info'])
            match result['category'].upper():
                case "PERNIKAHAN":
                    expiredEvent = datetime.fromtimestamp(result['detail_info']['reception_end']/1000)
                case "ULANG TAHUN":
                    expiredEvent = datetime.fromtimestamp(result['detail_info']['end']/1000)
                case "GRADUATION PARTY":
                    expiredEvent = datetime.fromtimestamp(result['detail_info']['end']/1000)
                case _:
                    expiredEvent = 0
                    print("Kategori tidak dikenali")
            # Validation Data ---------------------------------------- Finish

            # Insert Data ---------------------------------------- Start
            now = datetime.now()
            timestamp = int(round(time.time()*1000))
            query = GUEST_ADD_QUERY
            if expiredEvent > now:
                for guest in guests:
                    values = (user_id, accLevel, result['category_id'], invCode, guest['name'], guest['address'], guest['phone'], timestamp, user_id, timestamp, user_id)
                    DBHelper().save_data(query, values)
            else:
                return bad_request("Data tamu gagal ditambahkan karena acara telah berakhir.")
            # Insert Data ---------------------------------------- Finish

            # Log Activity Record ---------------------------------------- Start
            activity = f"User {user_name} menduplikat data tamu dari undangan {invitation['title']}."
            query = LOG_ADD_QUERY
            values = (user_id, accLevel, activity, timestamp, )
            DBHelper().save_data(query, values)
            # Log Activity Record ---------------------------------------- Finish

            # Return Response ======================================== 
            return success(statusCode=201)
        
        except Exception as e:
            return bad_request(str(e))
    # DUPLICATE GUEST ============================================================ End

    # IMPORT GUEST ============================================================ Begin
    # clear
    def import_guest(user_id, user_role, user_name, datas):   
        try:
            # Set Access Level ---------------------------------------- Start
            access = vld_role(user_role)
            accLevel = 2
            if access: # Access = True -> Admin
                return authorization_error()
            # Set Access Level ---------------------------------------- Finish

            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            requiredData = ["invitation_code", "file"]
            for req in requiredData:
                if req not in datas:
                    return parameter_error(f"Missing {req} in Request Body")
            # Checking Request Body ---------------------------------------- Finish

            # Initialize Data Input ---------------------------------------- Finish
            invCode = datas['invitation_code']
            file = datas['file']
            # Initialize Data Input ---------------------------------------- Finish

            # Checking Data ---------------------------------------- Start
            query = INV_CHK_CODE_QUERY
            values = (invCode,)
            result = DBHelper().get_data(query, values)
            if len(result) < 1:
                return not_found(f"Data undangan dengan kode {invCode} tidak dapat ditemukan.")
            result = result[0]
            # Checking Data ---------------------------------------- End

            # Read File ---------------------------------------- Start
            # Menambahkan padding jika diperlukan
            missing_padding = len(file) % 4
            if missing_padding:
                file += '=' * (4 - missing_padding)

            # Decode Base64 menjadi bytes
            file_bytes = base64.b64decode(file)
            
            # Membaca file Excel dari bytes menggunakan BytesIO
            try:
                # Coba dengan openpyxl (untuk .xlsx)
                excel_data = pd.read_excel(BytesIO(file_bytes), engine='openpyxl')
            except Exception as e1:
                # Jika gagal, coba dengan xlrd (untuk .xls)
                try:
                    excel_data = pd.read_excel(BytesIO(file_bytes), engine='xlrd')
                except Exception as e2:
                    return jsonify({'status': 'error', 'message': str(e2)})
            
            # Contoh: konversi DataFrame ke dictionary dan tampilkan sebagai JSON
            data_dict = excel_data.to_dict(orient='records')
            # Read File ---------------------------------------- End
            
            # Get Category Data ---------------------------------------- Start
            query = CTGR_GET_ALL_QUERY
            categories = DBHelper().execute(query)
            for category in categories:
                if category['id'] == result['category_id']:
                    result['category'] = category['category']
            # Get Category Data ---------------------------------------- End
            
            # Validation Data ---------------------------------------- Start
            result['detail_info'] = json.loads(result['detail_info'])
            match result['category'].upper():
                case "PERNIKAHAN":
                    expiredEvent = datetime.fromtimestamp(result['detail_info']['reception_end']/1000)
                case "ULANG TAHUN":
                    expiredEvent = datetime.fromtimestamp(result['detail_info']['end']/1000)
                case "GRADUATION PARTY":
                    expiredEvent = datetime.fromtimestamp(result['detail_info']['end']/1000)
                case _:
                    expiredEvent = 0
                    print("Kategori tidak dikenali")
            # Validation Data ---------------------------------------- Finish

            # Insert Data ---------------------------------------- Start
            now = datetime.now()
            timestamp = int(round(time.time()*1000))
            query = GUEST_ADD_QUERY
            if expiredEvent > now:
                for guest in data_dict:
                    print(guest)
                    values = (user_id, accLevel, result['category_id'], invCode, guest['name'], guest['address'], guest['phone'], timestamp, user_id, timestamp, user_id)
                    DBHelper().save_data(query, values)
            else:
                return bad_request("Data tamu gagal ditambahkan karena acara telah berakhir.")
            # Insert Data ---------------------------------------- Finish

            # Log Activity Record ---------------------------------------- Start
            activity = f"User {user_name} menambahkan data tamu dari import excel."
            query = LOG_ADD_QUERY
            values = (user_id, accLevel, activity, timestamp, )
            DBHelper().save_data(query, values)
            # Log Activity Record ---------------------------------------- Finish

            # Return Response ======================================== 
            return success_data(data_dict)
        
        except Exception as e:
            return bad_request(str(e))
    # IMPORT GUEST ============================================================ End
    
    # IMPORT GUEST ============================================================ Begin
    # clear
    def export_guest(user_id, user_role, datas):   
        try:
            # Set Access Level ---------------------------------------- Start
            access = vld_role(user_role)
            if access: # Access = True -> Admin
                return authorization_error()
            # Set Access Level ---------------------------------------- Finish

            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            if "invitation_code" not in datas:
                return parameter_error("Missing 'invitation_code' in Request Body.")
            
            invCode = datas["invitation_code"]
            if invCode == "":
                return defined_error("Id tamu tidak boleh kosong.", "Defined Error", 400)
            # Checking Request Body ---------------------------------------- Finish
            
            # Checking Data ---------------------------------------- Start
            query = INV_CHK_CODE_QUERY
            values = (invCode,)
            result = DBHelper().get_data(query, values)
            if len(result) < 1:
                return not_found(f"Data undangan dengan kode {invCode} tidak dapat ditemukan.")
            result = result[0]
            # Checking Data ---------------------------------------- End

            # Get Category Data ---------------------------------------- Start
            query = CTGR_GET_ALL_QUERY
            categories = DBHelper().execute(query)
            for category in categories:
                if category['id'] == result['category_id']:
                    result['category'] = category['category']
            # Get Category Data ---------------------------------------- End

            # Get Guest Data ---------------------------------------- Start
            query = GUEST_GET_BY_CODE_QUERY
            values = (invCode, )
            guests = DBHelper().get_data(query, values)
            if len(result) < 1:
                return not_found(f"Data Tamu dari undangan {result['title']} tidak dapat ditemukan.")
            # Get Guest Data ---------------------------------------- End

            # Collecting Data ---------------------------------------- Start
            dict_data = {
                "name": [],
                "address": [],
                "phone": []
            }
            for guest in guests:
                dict_data["name"].append(guest['name'])
                dict_data["address"].append(guest['address'])
                dict_data["phone"].append(guest['phone'])

            sheetFileName = secure_filename(time.strftime("%Y-%m-%d %H:%M:%S")+"_"+invCode+"_guest_list_"+user_id+".xlsx")
            file = pd.DataFrame(dict_data)
            file.to_excel(os.path.join(app.config['EXPORT_GUEST'], sheetFileName))
            # Collecting Data ---------------------------------------- Finish

            # Generate Invitation File URL ---------------------------------------- Start
            if len(result) >= 1:
                detailRequestURL = str(request.url).find('?')
                if detailRequestURL != -1:
                    index = detailRequestURL
                    request.url = request.url[:index]
            
            url_file = f"{request.url_root}guest/media/export/{sheetFileName}"
            # Generate Invitation File URL ---------------------------------------- Finish
            
            # Log Activity Record ---------------------------------------- Start
            response = {
                "url_file": url_file,
                "filename": sheetFileName
            }
            # Log Activity Record ---------------------------------------- Finish

            # Return Response ======================================== 
            return success_data(response)
        
        except Exception as e:
            return bad_request(str(e))
    # IMPORT GUEST ============================================================ End

    # GET ALL GUEST ============================================================ Begin
    # Clear
    def view_guest(user_id, user_role, user_name, datas):
        try:
            # Access Validation ======================================== 
            access = vld_role(user_role)

            # Checking Request Body ---------------------------------------- Start
            if access: # Access = True -> Admin
                if "user_id" not in datas:
                    return parameter_error("Missing 'user_id' in request body.")
                
                user_id = datas["user_id"]
                if user_id == "":
                    return defined_error("Id user tidak boleh kosong.", "Defined Error", 499)
            # Checking Request Body ---------------------------------------- Finish

            # Checking Data ---------------------------------------- Start
            query = GUEST_GET_BY_USR_QUERY
            values = (user_id, )
            result = DBHelper().get_data(query, values)
            if len(result) < 1:
                return not_found(f"Data tamu untuk user {user_name} tidak dapat ditemukan.")
            # Checking Data ---------------------------------------- Finish

            # Get Join Data ---------------------------------------- Start
            query = CTGR_GET_ALL_QUERY
            category = DBHelper().execute(query)
            query = INV_CHK_CODE_QUERY
            # Get Join Data ---------------------------------------- Finish

            # Set Join Data ---------------------------------------- Start
            for rsl in result:
                values = (rsl['invitation_code'], )
                invitation = DBHelper().get_data(query, values)
                for inv in invitation:
                    if rsl['invitation_code'] == inv['code']:
                        rsl['invitation_id'] = inv['id']
                for ctg in category:
                    if rsl['category_id'] == ctg['id']:
                        rsl['category'] = ctg['category']
            # Set Join Data ---------------------------------------- Finish

            # Response Data ---------------------------------------- Start
            response = []
            for rsl in result:
                data = {
                    "guest_id" : rsl["id"],
                    "category_id" : rsl['category_id'],
                    "invitation_id" : rsl['invitation_id'],
                    "guest_name" : rsl['name'],
                    "guest_phone" : rsl['phone'],
                    "event" : rsl['category'],
                    "invitation_code" : rsl["invitation_code"],
                    "owner" : user_id,
                    "owner_txt" : user_name,
                }
                response.append(data)
            # Response Data ---------------------------------------- Finish
            
            # Return Response ======================================== 
            return success_data(response)
        
        except Exception as e:
            return bad_request(str(e))
    # GET ALL GUEST ============================================================ End

    # # GET ALL GUEST ============================================================ Begin
    # def view_guest_by_user(user_id, user_role):
    #     try:
    #         # Access Validation ---------------------------------------- Start
    #         access, message = vld_role(user_role)
    #         if access: # True = Admin
    #             return defined_error("Hanya User yang dapat mengakses Menu ini.", "Forbidden", 403)
    #         # Access Validation ---------------------------------------- Finish

    #         # Checking Data ---------------------------------------- Start
    #         query = GUEST_GET_WITH_FILTER_QUERY
    #         values = (user_id,)
    #         result = DBHelper().get_data(query,values)
    #         if len(result) == 0 or result == None:
    #             return defined_error("Belum ada ucapan selamat dari calon tamu.", "Bad Request", 400)
    #         # Checking Data ---------------------------------------- Finish
            
    #         # Response Data ---------------------------------------- Start
    #         response = []
    #         for rsl in result:
    #             data = {
    #                 "greeting_id" : rsl["id"],
    #                 "name" : rsl["name"],
    #                 "email" : rsl["email"],
    #                 "greeting" : rsl["greeting"],
    #                 "invitation_code" : rsl["invitation_code"],
    #                 "user_owner" : rsl["user_id"],
    #                 "created_at": rsl["created_at"]
    #             }
    #             response.append(data)
    #         # Response Data ---------------------------------------- Finish
            
    #         # Return Response ======================================== 
    #         return success_data("Successed!", response)
        
    #     except Exception as e:
    #         return bad_request(str(e))
    # # GET ALL GUEST ============================================================ End

    # GET DETAIL GUEST ============================================================ Begin
    # Clear
    def view_detail_guest(user_role, datas):
        try:
            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            if "invitation_code" not in datas:
                return parameter_error("Missing 'invitation_code' in Request Body.")
            
            invCode = datas["invitation_code"]
            if invCode == "":
                return defined_error("Kode undangan tidak boleh kosong.", "Defined Error", 400)
            # Checking Request Body ---------------------------------------- Finish
            
            # Checking Data ---------------------------------------- Start
            query = GUEST_GET_BY_CODE_QUERY
            values = (invCode,)
            result = DBHelper().get_data(query, values)
            if len(result) < 1 :
                return not_found(f"Data tamu untuk kode undangan {invCode} tidak dapat ditemukan.")
            # Checking Data ---------------------------------------- Finish

            # Get Join Data ---------------------------------------- Start
            query = CTGR_GET_ALL_QUERY
            category = DBHelper().execute(query)
            query = INV_CHK_CODE_QUERY
            # Get Join Data ---------------------------------------- Finish

            # Set Join Data ---------------------------------------- Start
            for rsl in result:
                values = (rsl['invitation_code'], )
                invitation = DBHelper().get_data(query, values)
                for inv in invitation:
                    if rsl['invitation_code'] == inv['code']:
                        rsl['invitation_id'] = inv['id']
                for ctg in category:
                    if rsl['category_id'] == ctg['id']:
                        rsl['category'] = ctg['category']
            # Set Join Data ---------------------------------------- Finish

            # Response Data ---------------------------------------- Start
            response = []
            for rsl in result:
                createdAt = split_date_time(datetime.fromtimestamp(rsl["created_at"]/1000))
                updatedAt = split_date_time(datetime.fromtimestamp(rsl["updated_at"]/1000))
                data = {
                    "guest_id" : rsl["id"],
                    "category_id" : rsl["category_id"],
                    "invitation_id" : rsl["invitation_id"],
                    "event" : rsl["category"],
                    "name" : rsl["name"],
                    "phone" : rsl["phone"],
                    "address" : rsl["address"],
                    "invitation_code" : rsl["invitation_code"],
                    "user_owner" : rsl["user_id"],
                    "created_at": createdAt,
                    "updated_at": updatedAt
                }
                response.append(data)
            # Response Data ---------------------------------------- Finish

            # Return Response ======================================== 
            return success_data(response)
        
        except Exception as e:
            return bad_request(str(e))
    # GET DETAIL GUEST ============================================================ End

    # GET DETAIL GUEST ============================================================ Begin
    # Clear
    def view_guest_by_id(datas):
        try:
            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            if "guest_id" not in datas:
                return parameter_error("Missing 'guest_id' in Request Body.")
            
            guestId = datas["guest_id"]
            if guestId == "":
                return defined_error("Id tamu tidak boleh kosong.", "Defined Error", 400)
            # Checking Request Body ---------------------------------------- Finish
            
            # Checking Data ---------------------------------------- Start
            query = GUEST_GET_BY_ID_QUERY
            values = (guestId,)
            result = DBHelper().get_data(query, values)
            if len(result) < 1 :
                return defined_error(f"Data tamu untuk kode undangan {guestId} tidak dapat ditemukan.")
            # Checking Data ---------------------------------------- Finish
            
            # Set Category ---------------------------------------- Start
            query = CTGR_GET_ALL_QUERY
            category = DBHelper().execute(query)
            for ctg in category:
                for rsl in result:
                    if rsl['category_id'] == ctg['id']:
                        rsl['category'] = ctg['category']
            # Set Category ---------------------------------------- Finish

            # Response Data ---------------------------------------- Start
            rsl = result[0]
            createdAt = split_date_time(datetime.fromtimestamp(rsl["created_at"]/1000))
            updatedAt = split_date_time(datetime.fromtimestamp(rsl["updated_at"]/1000))
            response = {
                "guest_id" : rsl["id"],
                "category_id" : rsl["category_id"],
                "event" : rsl["category"],
                "name" : rsl["name"],
                "phone" : rsl["phone"],
                "address" : rsl["address"],
                "invitation_code" : rsl["invitation_code"],
                "user_owner" : rsl["user_id"],
                "created_at": createdAt,
                "updated_at": updatedAt
            }
            # Response Data ---------------------------------------- Finish

            # Return Response ======================================== 
            return success_data(response)
        
        except Exception as e:
            return bad_request(str(e))
    # GET DETAIL GUEST ============================================================ End

    # UPDATE GUEST ============================================================ Begin
    # Clear
    def edit_guest(user_id, user_role, datas):
        try:
            # Access Validation ---------------------------------------- Start
            access = vld_role(user_role)
            accLevel = 2
            # Access Validation ---------------------------------------- Finish

            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            requiredData = ["guest_id", "invitation_code", "name", "address", "phone"]
            for req in requiredData:
                if req not in datas:
                    return parameter_error(f"Missing {req} in Request Body")
            # Checking Request Body ---------------------------------------- Finish
            
            # Inisialize Data Input ---------------------------------------- Start
            gueId = datas["guest_id"]
            invCode = datas["invitation_code"]
            name = datas["name"]
            address = datas["address"]
            phone = datas["phone"]
            # Inisialize Data Input ---------------------------------------- Finish
            
            # Data Validation ---------------------------------------- Start
            query = GUEST_GET_BY_ID_QUERY
            values = (gueId, )
            result = DBHelper().get_data(query, values)
            if len(result) < 1 :
                return not_found("Data tamu tidak dapat ditemukan.")
            
            guestCheck, phone = vld_guest(name, address, phone, invCode, False)
            if len(guestCheck) != 0:
                return defined_error(guestCheck, "Bad Request", 400)
            # Data Validation ---------------------------------------- Finish
            
            # Update Data ---------------------------------------- Start
            timestamp = int(round(time.time()*1000))
            query = GUEST_UPDATE_QUERY
            values = (name, address, phone, timestamp, user_id, gueId, )
            DBHelper().save_data(query, values)
            # Update Data ---------------------------------------- Finish

            # Log Activity Record ---------------------------------------- Start
            activity = f"{user_role.title()} dengan id {user_id} mengubah data tamu {result[0]['name']}."
            query = LOG_ADD_QUERY
            values = (user_id, accLevel, activity, timestamp, )
            DBHelper().save_data(query, values)
            # Log Activity Record ---------------------------------------- Finish

            # Return Response ======================================== 
            return success(message="Updated!")
            
        except Exception as e:
            return bad_request(str(e))
    # UPDATE GUEST ============================================================ End

    # DELETE GUEST ============================================================ Begin
    # Clear
    def delete_guest(user_id, user_role, datas):     
        try:
            print(datas)
            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            if "guest_id" not in datas:
                return parameter_error("Missing 'guest_id' in Request Body.")
            
            guestId = datas["guest_id"]
            if guestId == "":
                return defined_error("Id tamu tidak boleh kosong.", "Defined Error", 400)
            # Checking Request Body ---------------------------------------- Finish
            
            # Data Validation ---------------------------------------- Start
            query = GUEST_GET_BY_ID_QUERY
            values = (guestId,)
            result = DBHelper().get_data(query, values)
            if len(result) < 1 :
                return not_found("Data tamu tidak dapat ditemukan.")
            # Data Validation ---------------------------------------- Finish

            # Delete Data ---------------------------------------- Start
            timestamp = int(round(time.time()*1000))
            query = GUEST_DELETE_QUERY
            values = (timestamp, user_id, guestId)
            DBHelper().save_data(query, values)
            # Delete Data ---------------------------------------- Finish

            # Log Activity Record ---------------------------------------- Start
            activity = f"User dengan id {user_id} menghapus data tamu {result[0]['name']}."
            query = LOG_ADD_QUERY
            values = (user_id, 2, activity, timestamp, )
            DBHelper().save_data(query, values)
            # Log Activity Record ---------------------------------------- Finish

            # Return Response ======================================== 
            return success("Deleted!")
            
        except Exception as e:
            return bad_request(str(e))
    # DELETE GUEST ============================================================ End

    # GET ROW-COUNT GUEST ============================================================ Begin
    # Clear
    def get_count_guest(user_id):
        try:
            # Get Data By User Id ---------------------------------------- Start
            query = GUEST_GET_BY_USR_QUERY
            values = (user_id, )
            result = DBHelper().get_count_filter_data(query, values)
            # Get Data By User Id ---------------------------------------- Finish

            # Checking Data ---------------------------------------- Start
            if result < 1 or result == None :
                return not_found("Data tamu tidak dapat ditemukan.")
            # Checking Data ---------------------------------------- Finish
            
            # Response Data ---------------------------------------- Start
            response = {
                "guest_count" : result
            }
            # Response Data ---------------------------------------- Finish

            # Return Response ======================================== 
            return success_data(response)
        
        except Exception as e:
            return bad_request(str(e))
    # GET ROW-COUNT GUEST ============================================================ End
# GUEST MODEL CLASS ============================================================ End