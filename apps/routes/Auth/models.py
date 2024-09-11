from flask import render_template, url_for, current_app as app
# from werkzeug.utils import secure_filename

from ...utilities.responseHelper import *
from ...utilities.dbHelper import DBHelper
from ...utilities.queries import *
from ...utilities.validator import *
from ...utilities.utils import *

import time, threading

# REQUEST TEMPLATE MODEL CLASS ============================================================ Begin
class AuthModels():
    # CREATE AUTH ============================================================ Begin
    # Clear
    def create_auth(datas):
        try:
            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            requiredData = ["user_id", "user_level", "email"]
            for req in requiredData:
                if req not in datas:
                    return parameter_error(f"Missing {req} in Request Body.")
            # Checking Request Body ---------------------------------------- Finish

            # Initialize Data Input ---------------------------------------- Start
            userId = datas["user_id"]
            userLevel = datas["user_level"]
            email = datas["email"]
            # Initialize Data Input ---------------------------------------- Finish

            # Data Validation ---------------------------------------- Start
            checkResult, token = vld_auth(email)
            if len(checkResult) != 0:
                return defined_error(checkResult, "Bad Request", statusCode=400)
            # Data Validation ---------------------------------------- Finish

            # Insert Data ---------------------------------------- Start
            timestamp = int(round(time.time()*1000))
            query = AUTH_ADD_QUERY
            values = (userId, userLevel, token, timestamp)
            resReturn = DBHelper().save_return(query, values)
            if resReturn is None:
                return defined_error("Gagal menyimpan data.", "Bad Request", 400)
            # Insert Data ---------------------------------------- Finish

            # Template Email ---------------------------------------- Start
            template_email = render_template(
                template_name_or_list="template_email.html",
                data={
                    "showGambar" : False,
                    "gambarURL" : app.config["BASE_URL"] + "/" + url_for("static", filename="icons/login.png"),
                    "judul" : "Verifikasi Akun Email",
                    "deskripsi" : "Terima kasih telah bergabung di aplikasi Creavitation. Silahkan aktifkan akun anda dengan menekan tombol dibawah ini",
                    "buttonLink" : app.config["FE_URL"] + f"/auth/verified/{token}",
                    "buttonText" : "Verifikasi Email"
                }
            )
            # Template Email ---------------------------------------- Finish

            # send mail
            email_sender(email, "Verify My Account", template_email)
            # def sending_email():
            #     email_sender(email, "Verify My Account", template_email)

            # # 🏃‍♀️ Optimasi API runtime dengan menjalankan fungsi sending_email secara parallel 
            # # Referensi : https://zoltan-varadi.medium.com/flask-api-how-to-return-response-but-continue-execution-828da40881e7
            # # Referensi : https://stackoverflow.com/questions/3221655/python-threading-string-arguments

            # thread = threading.Thread(target=sending_email)
            # thread.start()

            return success(statusCode=201)

        except Exception as e:
            print("error", e)
            return bad_request(str(e))
    # CREATE AUTH ============================================================ End
    
    # GET AUTH ============================================================ Begin
    def view_detail_auth(datas):
        try:
            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            if "token" not in datas:
                return parameter_error("Missing 'token' in Request Body.")
            
            token = datas["token"]
            if token == "":
                return defined_error("Token tidak boleh kosong.", "Defined Error", 400)
            # Checking Request Body ---------------------------------------- Finish

            # Get & Check Data ---------------------------------------- Start
            query = AUTH_GET_BY_TOKEN_QUERY
            values = (token, )
            result = DBHelper().get_data(query, values)
            if len(result) < 1:
                return not_found("Data autentikasi tidak dapat ditemukan.")
            result = result[0]
            # Get & Check Data ---------------------------------------- Finish
            
            # Response Data ---------------------------------------- Start
            createdAt = datetime.fromtimestamp(result['created_at']/1000)
            expiredAt = datetime.fromtimestamp(result['expired_at']/1000)
            now = datetime.now()
            response = {
                "auth_id" : result["id"],
                "user_id" : result["user_id"],
                "user_level" : result["user_level"],
                "token" : result["token"],
                "is_expired" : 1 if expiredAt < now else 0,
                "created_at" : createdAt,
                "expired_at" : expiredAt
            }
            # Response Data ---------------------------------------- Finish

            # Return Response ======================================== 
            return success_data(response)
        
        except Exception as e:
            return bad_request(str(e))
    # GET AUTH ============================================================ End

    # CREATE AUTH ============================================================ Begin
    def edit_auth(datas):
        try:
            # Checking Request Body ---------------------------------------- Start
            if datas == None:
                return invalid_params()
            
            requiredData = ["user_id", "user_level", "token"]
            for req in requiredData:
                if req not in datas:
                    return parameter_error(f"Missing {req} in Request Body.")
            # Checking Request Body ---------------------------------------- Finish

            # Initialize Data Input ---------------------------------------- Start
            userId = datas["user_id"]
            userLevel = datas["user_level"]
            token = datas["token"]
            # Initialize Data Input ---------------------------------------- Finish

            # Get & Check Data ---------------------------------------- Start
            query = AUTH_GET_BY_TOKEN_QUERY
            values = (token, )
            result = DBHelper().get_data(query, values)
            if len(result) < 1:
                return not_found("Data autentikasi tidak dapat ditemukan.")
            result = result[0]
            # Get & Check Data ---------------------------------------- Finish
            
            # Get & Check Data ---------------------------------------- Start
            query = USR_GET_BY_ID_QUERY
            values = (userId, )
            users = DBHelper().get_data(query, values)
            if len(users) < 1:
                return not_found("Data user tidak dapat ditemukan.")
            users = users[0]
            # Get & Check Data ---------------------------------------- Finish

            # Insert Data ---------------------------------------- Start
            token = auth_token()
            query = AUTH_UPDATE_QUERY
            values = (token, result['id'], )
            resReturn = DBHelper().save_return(query, values)
            if resReturn == None:
                return defined_error("Gagal mengubah data.", "Bad Request", 400)
            # Insert Data ---------------------------------------- Finish

            # Template Email ---------------------------------------- Start
            template_email = render_template(
                template_name_or_list="template_email.html",
                data={
                    "showGambar" : False,
                    "gambarURL" : app.config["BASE_URL"] + "/" + url_for("static", filename="icons/login.png"),
                    "judul" : "Verifikasi Akun Email",
                    "deskripsi" : "Terima kasih telah bergabung di aplikasi Creavitation. Silahkan aktifkan akun anda dengan menekan tombol dibawah ini",
                    "buttonLink" : app.config["FE_URL"] + f"/auth/verified/{token}",
                    "buttonText" : "Verifikasi Email"
                }
            )
            # Template Email ---------------------------------------- Finish

            # send mail
            email_sender(users['email'], "Verify My Account", template_email)
            # def sending_email():
            #     email_sender(users['email'], "Verify My Account", template_email)

            # # 🏃‍♀️ Optimasi API runtime dengan menjalankan fungsi sending_email secara parallel 
            # # Referensi : https://zoltan-varadi.medium.com/flask-api-how-to-return-response-but-continue-execution-828da40881e7
            # # Referensi : https://stackoverflow.com/questions/3221655/python-threading-string-arguments

            # thread = threading.Thread(target=sending_email)
            # thread.start()


            return success(message='Updated!')

        except Exception as e:
            print("error", e)
            return bad_request(str(e))
    # CREATE AUTH ============================================================ End
# REQUEST TEMPLATE MODEL CLASS ============================================================ Begin