from .queries import *
from .dbHelper import DBHelper
from .utils import *
from .templateData import *

from datetime import datetime, timedelta

import json


##########################################################################################################
# VALIDATION

# ACCOUNT VALIDATION ============================================================ Begin
def vld_admin_regis(name, email, password, repassword):
    checkResult = []

    if name == "":
        checkResult.append(f"Nama tidak boleh kosong")
    if email == "":
        checkResult.append(f"Email tidak boleh kosong")
    if password == "":
        checkResult.append(f"Password tidak boleh kosong")
    if repassword == "":
        checkResult.append(f"Password tidak boleh kosong")


    sanitName, charName = sanitize_all_char(name)
    if sanitName:
        checkResult.append(f"Nama tidak boleh mengandung karakter {charName}")
    sanitMail, charMail = sanitize_email_char(email)
    if sanitMail:
        checkResult.append(f"Email tidak boleh mengandung karakter {charMail}")
    sanitPass, charPass = sanitize_passwd_char(password)
    if sanitPass:
        checkResult.append(f"Password tidak boleh mengandung karakter {charPass}")
    sanitRepass, charRepass = sanitize_passwd_char(repassword)
    if sanitRepass:
        checkResult.append(f"Password tidak boleh mengandung karakter {charRepass}")


    if password != repassword:
        checkResult.append(f"Password tidak sama.")
    

    if string_checker(name):
        checkResult.append(f"Nama tidak valid.")
    if email_checker(email):
        checkResult.append(f"Email tidak valid.")
    passwordCheck, message = password_checker(password)
    if passwordCheck:
        checkResult.append(message)


    query = ADM_CHK_EMAIL_QUERY
    values = (email,)
    result = DBHelper().get_data(query, values)
    if len(result) != 0:
        checkResult.append(f"Email sudah terdaftar sebagai admin.")

    return checkResult 

def vld_user_regis(fname, mname, lname, phone, email, password, repassword):
    checkResult = []

    # Check Null String ---------------------------------------- Start
    if fname == "":
        checkResult.append(f"Nama tidak boleh kosong")
    if email == "":
        checkResult.append(f"Email tidak boleh kosong")
    if password == "":
        checkResult.append(f"Password tidak boleh kosong")
    if repassword == "":
        checkResult.append(f"Confirm password tidak boleh kosong.")
    # Check Null String ---------------------------------------- Finish

    # Sanitize String Input ---------------------------------------- Start
    sanitFName, charFName = sanitize_all_char(fname)
    if sanitFName:
        checkResult.append(f"Nama tidak boleh mengandung simbol {charFName}")
    sanitMail, charMail = sanitize_email_char(email)
    if sanitMail:
        checkResult.append(f"Email tidak boleh mengandung simbol {charMail}")
    sanitPass, charPass = sanitize_passwd_char(password)
    if sanitPass:
        checkResult.append(f"Password tidak boleh mengandung simbol '{charPass}'. Gunakan selain simbol '( ) [ ] < > ' ` \" ; . ,'.")
    sanitRepass, charRepass = sanitize_passwd_char(repassword)
    if sanitRepass:
        checkResult.append(f"Confirm password tidak boleh mengandung simbol '{charRepass}'. Gunakan selain simbol '( ) [ ] < > ' ` \" ; . ,'.")
    # Sanitize String Input ---------------------------------------- Finish

    # Comparing Password ======================================== 
    if password != repassword:
        checkResult.append(f"Password tidak sama.")
    
    # Filter String Input ---------------------------------------- Start
    if string_checker(fname):
        checkResult.append(f"Nama tidak valid.")
    if email_checker(email):
        checkResult.append(f"Email tidak valid.")
    passwordCheck, message = password_checker(password)
    if passwordCheck:
        checkResult.append(message)
    # Filter String Input ---------------------------------------- Finish

    # Checking Middle Name - If Ready ---------------------------------------- Start
    if mname != "":
        sanitMName, charMName = sanitize_all_char(mname)
        if sanitMName:
            checkResult.append(f"Nama tengah tidak boleh mengandung karakter '{charMName}'.")
        if string_checker(mname):
            checkResult.append(f"Nama tengah tidak valid.")
    # Checking Middle Name - If Ready ---------------------------------------- Finish

    # Checking Last Name - If Ready ---------------------------------------- Start
    if lname != "":
        sanitLName, charLName = sanitize_all_char(lname)
        if sanitLName:
            checkResult.append(f"Nama belakang tidak boleh mengandung karakter {charLName}")
        if string_checker(lname):
            checkResult.append(f"Nama belakang tidak valid.")
    # Checking Last Name - If Ready ---------------------------------------- Finish

    # Checking Phone Number - If Ready ---------------------------------------- Start
    if phone != "":
        sanitLName, charLName = sanitize_all_char(lname)
        if sanitLName:
            checkResult.append(f"Nama tidak boleh mengandung karakter {charLName}")
        if string_checker(lname):
            checkResult.append(f"Nama tidak valid.")
    # Checking Phone Number - If Ready ---------------------------------------- Finish

    # Checking Email on DB ---------------------------------------- Start
    query = USR_CHK_EMAIL_QUERY
    values = (email,)
    result = DBHelper().get_data(query, values)
    if len(result) != 0:
        checkResult.append(f"Email sudah terdaftar.")
    # Checking Email on DB ---------------------------------------- Finish

    # Return Checker ======================================== 
    return checkResult 

def vld_signin(email, password, level):
    checkResult = []

    if email == "":
        checkResult.append("Email tidak boleh kosong.")
    if password == "":
        checkResult.append("Password tidak boleh kosong.")

    sanitMail, charMail = sanitize_email_char(email)
    if sanitMail:
        checkResult.append(f"Email tidak boleh mengandung karakter {charMail}.")
    sanitPass, charPass = sanitize_passwd_char(password)
    if sanitPass:
        checkResult.append(f"Password tidak boleh mengandung karakter {charPass}.")
    
    if email_checker(email):
        checkResult.append("Email tidak valid.")
    
    # Cek Role
    values = (email,)
    query = ADM_CHK_EMAIL_QUERY if level == 1 else USR_CHK_EMAIL_QUERY
    result = DBHelper().get_data(query, values)
    
    # Cek data email ready or not
    stts = 200
    if len(result) == 0 or result == None:
        stts = 404
        checkResult.append("Email belum terdaftar.")
    
    # Cek password
    if len(result) != 0:
        savedPassword = result[0]['password']
        validatePass = password_compare(savedPassword, password)
        if not validatePass:
            stts = 400
            checkResult.append("Akun tidak valid.")
    
    # Get photo profile
    query = PROF_GET_BY_ID_QUERY
    values = (result[0]['id'], level)
    profile = DBHelper().get_data(query, values)
    result[0]['photos'] = profile[0]['photos']
    
    return checkResult, result, stts

def vld_profile(userId, userLevel, fName, mName, lName, phone):
    checkResult = []
 
    # Validation For First Name ---------------------------------------- Start
    if fName == "":
        # Sanitize String Input ======================================== 
        sanitFName, charFName = sanitize_all_char(fName)
        if sanitFName:
            checkResult.append(f"Nama tidak boleh mengandung karakter {charFName}")

        # Filter String Input ======================================== 
        if string_checker(mName):
            checkResult.append(f"Nama tidak valid.")
    # Validation For First Name ---------------------------------------- Finish

    # Validation For Middle Name - If Set ---------------------------------------- Start
    if mName != "":
        # Sanitize String Input ======================================== 
        sanitMName, charMName = sanitize_all_char(mName)
        if sanitMName:
            checkResult.append(f"Nama tidak boleh mengandung karakter {charMName}")

        # Filter String Input ======================================== 
        if string_checker(mName):
            checkResult.append(f"Nama tidak valid.")
    # Validation For Middle Name - If Set ---------------------------------------- Finish
    
    # Validation For Last Name - If Set ---------------------------------------- Start
    if lName != "":
        # Sanitize String Input ======================================== 
        sanitLName, charLName = sanitize_all_char(lName)
        if sanitLName:
            checkResult.append(f"Nama tidak boleh mengandung karakter {charLName}")

        # Filter String Input ======================================== 
        if string_checker(lName):
            checkResult.append(f"Nama tidak valid.")
    # Validation For Last Name - If Set ---------------------------------------- Finish

    # Validation For Phone - If Set ---------------------------------------- Start
    if (phone != "") or (phone != 0):
        # Sanitize Integer Input ======================================== 
        sanitPhone, charPhone = sanitize_all_char(phone)
        if sanitPhone:
            checkResult.append(f"Phone tidak boleh mengandung karakter {charPhone}")

        # Filter Integer Input ======================================== 
        if phone_checker(phone):
            checkResult.append(f"Phone tidak valid.")
    # Validation For Phone - If Set ---------------------------------------- Finish

    # Checking Email on DB ---------------------------------------- Start
    query = PROF_CHECK_QUERY
    values = (userId, userLevel, )
    result = DBHelper().get_data(query, values)
    if (len(result) == 0) or (result == None):
        checkResult.append(f"Profile user tidak ditemukan.")
    # Checking Email on DB ---------------------------------------- Finish

    # Return Checker ======================================== 
    return checkResult, result
# ACCOUNT VALIDATION ============================================================ End

# ROLE VALIDATION ============================================================ Begin
def vld_role(role):
    access = False

    if role.upper() == "ADMIN":
        access = True

    return access
# ROLE VALIDATION ============================================================ End

# CATEGORY VALIDATION ============================================================ Begin
def vld_category(category, format_data, is_create=True):
    checkResult = []

    # Check Null Value ---------------------------------------- Start
    if category == "":
        checkResult.append("Kategori tidak boleh kosong")
    if type(format_data) != dict:
        checkResult.append("Format data tidak valid")
    if format_data is None or len(format_data) < 1:
        checkResult.append("Format data undangan tidak boleh kosong")
    # Check Null Value ---------------------------------------- Finish

    # Sanitize Category ---------------------------------------- Start
    sanitCtgr, charCtgr = sanitize_all_char(category)
    if sanitCtgr:
        checkResult.append(f"Kategori tidak boleh mengandung karakter {charCtgr}")
    # Sanitize Category ---------------------------------------- Finish
    
    # Check String Value ---------------------------------------- Start
    if string_checker(category):
        checkResult.append("Kategori tidak valid")
    # Check String Value ---------------------------------------- Finish

    # Check Duplicate Category ---------------------------------------- Start
    # mandatory = ["name", "date", "time", "location"]
    # for default in mandatory:
    #     if default not in format_data:
    #         checkResult.append(f"Minimal tambahkan format {default}")
    # Check Duplicate Category ---------------------------------------- Finish

    # Check Duplicate Category ---------------------------------------- Start
    if is_create:
        query = CTGR_CHK_QUERY
        values = (category,)
        result = DBHelper().get_count_filter_data(query, values)
        if result > 0:
            checkResult.append("Kategori sudah terdaftar")
    # Check Duplicate Category ---------------------------------------- Finish

    return checkResult
# CATEGORY VALIDATION ============================================================ End

# GUEST VALIDATION ============================================================ Begin
def vld_guest(name, address, phone, invCode, is_create=True):
    checkResult = []

    if name == "":
        checkResult.append(f"Nama tidak boleh kosong.")
    if address == "":
        checkResult.append(f"Alamat tidak boleh kosong.")
    if phone == "":
        checkResult.append(f"Nomor handphone tidak boleh kosong.")


    sanitName, charName = sanitize_all_char(name)
    if sanitName:
        checkResult.append(f"Nama tidak boleh mengandung karakter {charName}.")
    sanitPhone, charPhone = sanitize_phone_char(phone)
    if sanitPhone:
        checkResult.append(f"Nomor handphone tidak boleh mengandung karakter {charPhone}.")
        
    
    if string_checker(name):
        checkResult.append(f"Nama tidak valid")
    if phone_checker(phone):
        checkResult.append(f"Nomor handphone tidak valid")
    
    if phone != "":
        if phone[0] == "0":
            phone = "62"+phone[1:]

    if is_create:
        query = GUEST_CHK_QUERY
        values = (invCode, phone, )
        result = DBHelper().get_count_filter_data(query, values)
        if result > 0 :
            checkResult.append(f"Data tamu dengan nomor telepon '{phone}' telah terdaftar.")

    return checkResult, phone
# GUEST VALIDATION ============================================================ End

# GREETING VALIDATION ============================================================ Begin
def vld_greeting(invCode, name, status, greeting):
    checkResult = []

    if name == "":
        checkResult.append("Nama tidak boleh kosong.")
    if status == "":
        checkResult.append("Konfirmasi kehadiran tidak boleh kosong")
    if greeting == "":
        checkResult.append("Pesan tidak boleh kosong.")


    sanitName, charName = sanitize_all_char(name)
    if sanitName:
        checkResult.append(f"Nama tidak boleh mengandung karakter {charName}")
        
    
    if string_checker(name):
        checkResult.append("Nama tidak valid.")
    
    
    query = INV_CHK_CODE_QUERY
    values = (invCode,)
    result = DBHelper().get_data(query, values)
    if len(result) < 1:
        checkResult.append("Data Undangan tidak dapat ditemukan.")

    return checkResult 
# GREETING VALIDATION ============================================================ End

# TEMPLATE VALIDATION ============================================================ Begin
def vld_template(title, thumbnail, css, js, wallpaper1, wallpaper2, category, is_create=True):
    checkResult = []

    if title == "":
        checkResult.append(f"Judul template tidak boleh kosong.")
    if thumbnail == "":
        checkResult.append(f"Thumbnail tidak boleh kosong.")
    if css == "":
        checkResult.append(f"Css tidak boleh kosong.")
    if wallpaper1 == "":
        checkResult.append(f"Wallpaper 1 tidak boleh kosong.")
    if wallpaper2 == "":
        checkResult.append("Wallpaper 2 tidak boleh kosong.")
    if category == "0":
        checkResult.append("Kategori tidak boleh kosong.")
    
    # Sanitize Title ---------------------------------------- Start
    sanitTitle, charTitle = sanitize_title_char(title)
    if sanitTitle:
        checkResult.append(f"Judul tidak boleh mengandung karakter {charTitle}.")
    # Sanitize Title ---------------------------------------- Finish
    
    if is_create:
        query = TMPLT_CHK_QUERY
        values = (title,)
        result = DBHelper().get_count_filter_data(query, values)
        if result != 0:
            checkResult.append("Judul sudah terdaftar.")

        # Photo Check ---------------------------------------- Start
        if thumbnail != "":
            # Memisahkan bagian 'data:' dari base64 string
            header, encoded = thumbnail.split(',', 1)
            # Memisahkan 'data:' dan mengambil MIME type
            mime_type = header.split(':')[1].split(';')[0].split('/')[0]
            if mime_type != "image":
                checkResult.append("File thumbnail yang diinputkan harus berupa gambar.")

        
        if css != "":
            # Memisahkan bagian 'data:' dari base64 string
            header, encoded = css.split(',', 1)
            # Memisahkan 'data:' dan mengambil MIME type
            mime_type = header.split(':')[1].split(';')[0]

            if mime_type != "text/css":
                checkResult.append("File css yang diinputkan harus berupa gambar.")
        
        
        if js != "":
            # Memisahkan bagian 'data:' dari base64 string
            header, encoded = js.split(',', 1)
            # Memisahkan 'data:' dan mengambil MIME type
            mime_type = header.split(':')[1].split(';')[0]
 
            if mime_type != "text/javascript":
                checkResult.append("File javascript yang diinputkan harus berupa gambar.")

        
        if wallpaper1 != "":
            # Memisahkan bagian 'data:' dari base64 string
            header, encoded = wallpaper1.split(',', 1)
            # Memisahkan 'data:' dan mengambil MIME type
            mime_type = header.split(':')[1].split(';')[0].split('/')[0]
            if mime_type != "image":
                checkResult.append("File wallpaper yang diinputkan harus berupa gambar.")

        
        if wallpaper2 != "":
            # Memisahkan bagian 'data:' dari base64 string
            header, encoded = wallpaper2.split(',', 1)
            # Memisahkan 'data:' dan mengambil MIME type
            mime_type = header.split(':')[1].split(';')[0].split('/')[0]
            if mime_type != "image":
                checkResult.append("File wallpaper yang diinputkan harus berupa gambar.")
        # Photo Check ---------------------------------------- Finish
        
    randomNumber = str(random_number(5))

    return checkResult, randomNumber

def vld_request_template(design, deadline, categoryId):
    checkResult = []

    # Input Check ---------------------------------------- Start
    if int(categoryId) == 0:
        checkResult.append("Kategori tidak boleh kosong.")
    if design == "":
        checkResult.append("Desain tidak boleh kosong.")
    if deadline == "":
        checkResult.append("Batas waktu tidak boleh kosong.")
    # Input Check ---------------------------------------- Finish

    # Datetime Check ---------------------------------------- Start
    if deadline != "":
        deadline = datetime.strptime(deadline, "%d %B %Y")
        now = datetime.now()
        oneweek = now + timedelta(days=6)
        if deadline < now:
            checkResult.append("Batas waktu yang diinputkan sudah terlewat.")
        elif deadline < oneweek:
            checkResult.append("Batas waktu minimal 7 hari dari sekarang.")
    # Datetime Check ---------------------------------------- Finish

    # Photo Check ---------------------------------------- Start
    if design != "":
        # Memisahkan bagian 'data:' dari base64 string
        header, encoded = design.split(',', 1)
        # Memisahkan 'data:' dan mengambil MIME type
        mime_type = header.split(':')[1].split(';')[0].split('/')[0]
        if mime_type != "image":
            checkResult.append("Data desain yang diinputkan harus berupa gambar.")
    # Photo Check ---------------------------------------- Finish
    
    return checkResult

# TEMPLATE VALIDATION ============================================================ End

# INVITATION VALIDATION ============================================================ Begin
def vld_invitation_code():
    invCode = str(random_string_number(6))

    # Check Code ---------------------------------------- Start
    query = INV_CHK_CODE_QUERY
    values = (invCode, )
    result = DBHelper().get_count_filter_data(query, values)
    if result > 0:
        return vld_invitation_code()
    # Check Code ---------------------------------------- Finish

    # Return Value ========================================
    return invCode

def vld_invitation(userId, categoryId, templateId, title, personalData, detailInfo):
    checkResult = []

    # Validation Null Data ---------------------------------------- Start
    if title == "":
        checkResult.append(f"Judul template tidak boleh kosong.")
    if personalData == None:
        checkResult.append(f"Data pribadi tidak boleh kosong tidak boleh kosong.")
    if detailInfo == None:
        checkResult.append(f"Data acara tidak boleh kosong tidak boleh kosong.")
    # Validation Null Data ---------------------------------------- Finish
    
    # Check Data Title & Template ---------------------------------------- Start
    # Template
    query = TMPLT_GET_BY_ID_QUERY
    values = (templateId,)
    ckTemplate = DBHelper().get_count_filter_data(query, values)
    if ckTemplate < 1:
        checkResult.append(f"Data template tidak dapat ditemukan.")
    # Title
    query = INV_CHK_TITLE_QUERY
    values = (title, )
    ckInvit = DBHelper().get_count_filter_data(query, values)
    if ckInvit > 0:
        checkResult.append(f"Judul sudah terpakai.")
    # Check Data Title & Template ---------------------------------------- Finish
    
    # Sanitize Title ---------------------------------------- Start
    sanitTitle, charTitle = sanitize_title_char(title)
    if sanitTitle:
        checkResult.append(f"Judul tidak boleh mengandung karakter {charTitle}.")
    # Sanitize Title ---------------------------------------- Finish
    
    # String Filter ---------------------------------------- Start
    if string_checker(title):
        checkResult.append(f"Judul tidak valid.")
    # String Filter ---------------------------------------- Finish
    
    # Check Data Category ---------------------------------------- Start
    query = CTGR_GET_BY_ID_QUERY
    values = (categoryId,)
    ckCategory = DBHelper().get_data(query, values)
    if len(ckCategory) < 1:
        checkResult.append(f"Data kategori tidak dapat ditemukan.")
    # Check Data Category ---------------------------------------- Finish

    # Check Detail Data ---------------------------------------- Start
    detail = True
    if len(detailInfo) < 1:
        detail = False
        checkResult.append("Info acara tidak boleh kosong.")
    personData = True
    if len(personalData) < 1:
        personData = False
        checkResult.append("Data diri tidak boleh kosong.")
    # Check Detail Data ---------------------------------------- Finish

    # Create Invitation Code ========================================
    invCode = vld_invitation_code()

    # Check By Category ---------------------------------------- Start
    # Wedding
    if ckCategory[0]['category'].upper() == "PERNIKAHAN":
        print("kategori => ", ckCategory[0]['category'].upper())
        # Check Detail Info ---------------------------------------- Start
        if detail:
            marriageDate = detailInfo["marriage_date"]
            marriageStart = detailInfo["marriage_start"]
            marriageEnd = detailInfo["marriage_end"]
            receptionDate = detailInfo["reception_date"]
            receptionStart = detailInfo["reception_start"]
            receptionEnd = detailInfo["reception_end"]
            now = datetime.now()

            # Akad
            if marriageDate != "":
                marriageDate = datetime.strptime(marriageDate, "%d %B %Y")
                marriageStart = datetime.strptime(marriageStart, "%I:%M %p")
                mergeDTS = datetime.combine(datetime.date(marriageDate), datetime.time(marriageStart))
                if mergeDTS <= now:
                    checkResult.append("Tanggal yang diinputkan sudah terlewat.")

                if marriageEnd != "1":
                    marriageEnd = datetime.strptime(marriageEnd, "%I:%M %p")
                    mergeDTE = datetime.combine(datetime.date(marriageDate), datetime.time(marriageEnd))
                    if mergeDTS >= mergeDTE:
                        checkResult.append("Waktu akad yang anda masukkan tidak valid.")
                    detailInfo['marriage_end'] = int(round(datetime.timestamp(mergeDTE)*1000))

                detailInfo["marriage_date"] = datetime.strftime(marriageDate, "%d %B %Y")
                detailInfo["marriage_start"] = int(round(datetime.timestamp(mergeDTS)*1000))

            # Resepsi
            if receptionDate != "":
                receptionDate = datetime.strptime(receptionDate, "%d %B %Y")
                receptionStart = datetime.strptime(receptionStart, "%I:%M %p")
                mergeDTS = datetime.combine(datetime.date(receptionDate), datetime.time(receptionStart))
                if mergeDTS <= now:
                    checkResult.append("Tanggal yang diinputkan sudah terlewat.")

                if receptionEnd != "1":
                    receptionEnd = datetime.strptime(receptionEnd, "%I:%M %p")
                    mergeDTE = datetime.combine(datetime.date(receptionDate), datetime.time(receptionEnd))
                    if mergeDTS >= mergeDTE:
                        checkResult.append("Waktu resepsi yang anda masukkan tidak valid.")
                    detailInfo['reception_end'] = int(round(datetime.timestamp(mergeDTE)*1000))

                detailInfo["reception_date"] = datetime.strftime(receptionDate, "%d %B %Y")
                detailInfo["reception_start"] = int(round(datetime.timestamp(mergeDTS)*1000))
        # Check Detail Info ---------------------------------------- Finish

        # Check Personal Data ---------------------------------------- Start
        if personData:
            mansPhotos = personalData["mans_photo"]
            womansPhotos = personalData["womans_photo"]
            if mansPhotos != "":
                # Memisahkan bagian 'data:' dari base64 string
                mheader, mencoded = mansPhotos.split(',', 1)
                # Memisahkan 'data:' dan mengambil MIME type
                mime_type = mheader.split(':')[1].split(';')[0].split('/')[0]
                if mime_type != "image":
                    checkResult.append("Data foto yang diinputkan harus berupa gambar.")
                else:
                    # Saving File ---------------------------------------- Start
                    mpFileName = secure_filename(time.strftime("%Y-%m-%d %H:%M:%S")+"_"+invCode+"_man_photo_"+userId+".jpg")
                    mpPath = os.path.join(app.config['USER_INVITATION_FILE'], mpFileName)
                    saving_image(mansPhotos, mpPath)
                    personalData['mans_photo'] = mpFileName
                    # Saving File ---------------------------------------- Finish
            else:
                checkResult.append("Foto mempelai pria tidak boleh kosong.")
            
            if womansPhotos != "":
                wheader, wencoded = womansPhotos.split(',', 1)
                mime_type = wheader.split(':')[1].split(';')[0].split('/')[0]
                if mime_type != "image":
                    checkResult.append("Data foto yang diinputkan harus berupa gambar.")
                else:
                    # Saving File ---------------------------------------- Start
                    wpFileName = secure_filename(time.strftime("%Y-%m-%d %H:%M:%S")+"_"+invCode+"_woman_photo_"+userId+".jpg")
                    wpPath = os.path.join(app.config['USER_INVITATION_FILE'], wpFileName)
                    saving_image(womansPhotos, wpPath)
                    personalData['womans_photo'] = wpFileName
                    # Saving File ---------------------------------------- Finish
            else:
                checkResult.append("Foto mempelai wanita tidak boleh kosong.")
        # Check Personal Data ---------------------------------------- Finish

    # Birthday
    elif ckCategory[0]['category'].upper() == "ULANG TAHUN":
        print("kategori => ", ckCategory[0]['category'].upper())
        # Check Detail Info ---------------------------------------- Start
        if detail:
            dates = detailInfo["date"]
            starts = detailInfo["start"]
            ends = detailInfo["end"]
            now = datetime.now()

            # Akad
            if dates != "":
                dates = datetime.strptime(dates, "%d %B %Y")
                starts = datetime.strptime(starts, "%I:%M %p")
                mergeDTS = datetime.combine(datetime.date(dates), datetime.time(starts))
                if mergeDTS <= now:
                    checkResult.append("Tanggal yang diinputkan sudah terlewat.")

                if ends != "1":
                    ends = datetime.strptime(ends, "%I:%M %p")
                    mergeDTE = datetime.combine(datetime.date(dates), datetime.time(ends))
                    if mergeDTS >= mergeDTE:
                        checkResult.append("Waktu akad yang anda masukkan tidak valid.")
                    detailInfo['end'] = int(round(datetime.timestamp(mergeDTE)*1000))

                detailInfo["date"] = datetime.strftime(dates, "%d %B %Y")
                detailInfo["start"] = int(round(datetime.timestamp(mergeDTS)*1000))
        # Check Detail Info ---------------------------------------- Finish

        # Check Personal Data ---------------------------------------- Start
        if personData:
            myphoto = personalData["myphoto"]
            if myphoto != "":
                # Memisahkan bagian 'data:' dari base64 string
                mheader, mencoded = myphoto.split(',', 1)
                # Memisahkan 'data:' dan mengambil MIME type
                mime_type = mheader.split(':')[1].split(';')[0].split('/')[0]
                if mime_type != "image":
                    checkResult.append("Data foto yang diinputkan harus berupa gambar.")
                else:
                    # Saving File ---------------------------------------- Start
                    pFName = secure_filename(time.strftime("%Y-%m-%d %H:%M:%S")+"_"+invCode+"_mybd_photo_"+userId+".jpg")
                    photoPath = os.path.join(app.config['USER_INVITATION_FILE'], pFName)
                    saving_image(myphoto, photoPath)
                    personalData['myphoto'] = pFName
                    # Saving File ---------------------------------------- Finish
            else:
                checkResult.append("Foto anda tidak boleh kosong.")
        # Check Personal Data ---------------------------------------- Finish
    # Check By Category ---------------------------------------- Finish

    # Return Value ========================================
    return checkResult, personalData, detailInfo, invCode

def vld_edit_invitation(result, title, personalData, detailInfo):
    checkResult = []

    oldData = result[0]
    oldData['personal_data'] = json.loads(oldData['personal_data'])
    oldData['detail_info'] = json.loads(oldData['detail_info'])
    # Validation Null Data ---------------------------------------- Start
    if title == "":
        checkResult.append(f"Judul template tidak boleh kosong.")
    if personalData == None:
        checkResult.append(f"Data pribadi tidak boleh kosong tidak boleh kosong.")
    if detailInfo == None:
        checkResult.append(f"Data acara tidak boleh kosong tidak boleh kosong.")
    # # Validation Null Data ---------------------------------------- Finish
    
    # Check Data Title & Template ---------------------------------------- Start
    # Template
    query = TMPLT_GET_BY_ID_QUERY
    values = (oldData['template_id'],)
    ckTemplate = DBHelper().get_count_filter_data(query, values)
    if ckTemplate < 1:
        checkResult.append(f"Data template tidak dapat ditemukan.")
    # Check Data Title & Template ---------------------------------------- Finish
    
    # Sanitize Title ---------------------------------------- Start
    sanitTitle, charTitle = sanitize_title_char(title)
    if sanitTitle:
        checkResult.append(f"Judul tidak boleh mengandung karakter {charTitle}.")
    # Sanitize Title ---------------------------------------- Finish
    
    # String Filter ---------------------------------------- Start
    if string_checker(title):
        checkResult.append(f"Judul tidak valid.")
    # String Filter ---------------------------------------- Finish
    
    # Check Data Category ---------------------------------------- Start
    query = CTGR_GET_BY_ID_QUERY
    values = (oldData['category_id'],)
    ckCategory = DBHelper().get_data(query, values)
    if len(ckCategory) < 1:
        checkResult.append(f"Data kategori tidak dapat ditemukan.")
    # Check Data Category ---------------------------------------- Finish

    # Check Detail Data ---------------------------------------- Start
    detail = True
    if len(detailInfo) < 1:
        detail = False
        checkResult.append("Info acara tidak boleh kosong.")
    personData = True
    if len(personalData) < 1:
        personData = False
        checkResult.append("Info acara tidak boleh kosong.")
    # Check Detail Data ---------------------------------------- Finish

    # Check By Category ---------------------------------------- Start
    # Wedding
    if ckCategory[0]['category'].upper() == "PERNIKAHAN":
        print("kategori => ", ckCategory[0]['category'].upper())
        # Check Detail Info ---------------------------------------- Start
        if detail:
            marriageDate = detailInfo["marriage_date"]
            marriageStart = detailInfo["marriage_start"]
            marriageEnd = detailInfo["marriage_end"]
            receptionDate = detailInfo["reception_date"]
            receptionStart = detailInfo["reception_start"]
            receptionEnd = detailInfo["reception_end"]
            now = datetime.now()

            # Akad
            if marriageDate != "":
                marriageDate = datetime.strptime(marriageDate, "%d %B %Y")
                marriageStart = datetime.strptime(marriageStart, "%I:%M %p")
                mergeDTS = datetime.combine(datetime.date(marriageDate), datetime.time(marriageStart))
                if mergeDTS <= now:
                    checkResult.append("Tanggal yang diinputkan sudah terlewat.")

                if marriageEnd != "1":
                    marriageEnd = datetime.strptime(marriageEnd, "%I:%M %p")
                    mergeDTE = datetime.combine(datetime.date(marriageDate), datetime.time(marriageEnd))
                    if mergeDTS >= mergeDTE:
                        checkResult.append("Waktu akad yang anda masukkan tidak valid.")
                    detailInfo['marriage_end'] = int(round(datetime.timestamp(mergeDTE)*1000))

                detailInfo["marriage_date"] = datetime.strftime(marriageDate, "%d %B %Y")
                detailInfo["marriage_start"] = int(round(datetime.timestamp(mergeDTS)*1000))
            else:
                checkResult.append("Data tanggal tidak boleh kosong")

            # Resepsi
            if receptionDate != "":
                receptionDate = datetime.strptime(receptionDate, "%d %B %Y")
                receptionStart = datetime.strptime(receptionStart, "%I:%M %p")
                mergeDTS = datetime.combine(datetime.date(receptionDate), datetime.time(receptionStart))
                if mergeDTS <= now:
                    checkResult.append("Tanggal yang diinputkan sudah terlewat.")

                if receptionEnd != "1":
                    receptionEnd = datetime.strptime(receptionEnd, "%I:%M %p")
                    mergeDTE = datetime.combine(datetime.date(receptionDate), datetime.time(receptionEnd))
                    if mergeDTS >= mergeDTE:
                        checkResult.append("Waktu resepsi yang anda masukkan tidak valid.")
                    detailInfo['reception_end'] = int(round(datetime.timestamp(mergeDTE)*1000))

                detailInfo["reception_date"] = datetime.strftime(receptionDate, "%d %B %Y")
                detailInfo["reception_start"] = int(round(datetime.timestamp(mergeDTS)*1000))
            else:
                checkResult.append("Data tanggal tidak boleh kosong")
        # Check Detail Info ---------------------------------------- Finish

        # Check Personal Data ---------------------------------------- Start
        if personData:
            mansPhotos = personalData["mans_photo"]
            womansPhotos = personalData["womans_photo"]
            if mansPhotos != oldData['personal_data']['mans_photo']:
                # Memisahkan bagian 'data:' dari base64 string
                mheader, mencoded = mansPhotos.split(',', 1)
                # Memisahkan 'data:' dan mengambil MIME type
                mime_type = mheader.split(':')[1].split(';')[0].split('/')[0]
                if mime_type != "image":
                    checkResult.append("Data foto yang diinputkan harus berupa gambar.")
                else:
                    mpFileName = secure_filename(time.strftime("%Y-%m-%d %H:%M:%S")+"_"+oldData['code']+"_man_photo_"+str(oldData['user_id'])+".jpg")
                    mpPath = os.path.join(app.config['USER_INVITATION_FILE'], mpFileName)
                    saving_image(personalData['mans_photo'], mpPath)
                    personalData['mans_photo'] = mpFileName
                
            if womansPhotos != oldData['personal_data']['womans_photo']:
                wheader, wencoded = womansPhotos.split(',', 1)
                mime_type = wheader.split(':')[1].split(';')[0].split('/')[0]
                if mime_type != "image":
                    checkResult.append("Data foto yang diinputkan harus berupa gambar.")
                else:
                    wpFileName = secure_filename(time.strftime("%Y-%m-%d %H:%M:%S")+"_"+oldData['code']+"_woman_photo_"+str(oldData['user_id'])+".jpg")
                    wpPath = os.path.join(app.config['USER_INVITATION_FILE'], wpFileName)
                    saving_image(personalData['womans_photo'], wpPath)
                    personalData['womans_photo'] = wpFileName
        # Check Personal Data ---------------------------------------- Finish
    
    # Birthday
    elif ckCategory[0]['category'].upper() == "ULANG TAHUN":
        print("kategori => ", ckCategory[0]['category'].upper())
        # Check Detail Info ---------------------------------------- Start
        if detail:
            dates = detailInfo["date"]
            starts = detailInfo["start"]
            ends = detailInfo["end"]
            now = datetime.now()

            # Akad
            if dates != "":
                dates = datetime.strptime(dates, "%d %B %Y")
                starts = datetime.strptime(starts, "%I:%M %p")
                mergeDTS = datetime.combine(datetime.date(dates), datetime.time(starts))
                if mergeDTS <= now:
                    checkResult.append("Tanggal yang diinputkan sudah terlewat.")

                if ends != "1":
                    ends = datetime.strptime(ends, "%I:%M %p")
                    mergeDTE = datetime.combine(datetime.date(dates), datetime.time(ends))
                    if mergeDTS >= mergeDTE:
                        checkResult.append("Waktu akad yang anda masukkan tidak valid.")
                    detailInfo['end'] = int(round(datetime.timestamp(mergeDTE)*1000))

                detailInfo["date"] = datetime.strftime(dates, "%d %B %Y")
                detailInfo["start"] = int(round(datetime.timestamp(mergeDTS)*1000))
        # Check Detail Info ---------------------------------------- Finish

        # Check Personal Data ---------------------------------------- Start
        if personData:
            myphoto = personalData["myphoto"]
            if myphoto != oldData['personal_data']['myphoto']:
                # Memisahkan bagian 'data:' dari base64 string
                mheader, mencoded = myphoto.split(',', 1)
                # Memisahkan 'data:' dan mengambil MIME type
                mime_type = mheader.split(':')[1].split(';')[0].split('/')[0]
                if mime_type != "image":
                    checkResult.append("Data foto yang diinputkan harus berupa gambar.")
                else:
                    # Saving File ---------------------------------------- Start
                    pFName = secure_filename(time.strftime("%Y-%m-%d %H:%M:%S")+"_"+oldData['code']+"_photo_"+str(oldData['user_id'])+".jpg")
                    photoPath = os.path.join(app.config['USER_INVITATION_FILE'], pFName)
                    saving_image(myphoto, photoPath)
                    personalData['myphoto'] = pFName
                    # Saving File ---------------------------------------- Finish
        # Check Personal Data ---------------------------------------- Finish
    # Check By Category ---------------------------------------- Finish

    # Return Value ========================================
    return checkResult, personalData, detailInfo
# INVITATION VALIDATION ============================================================ End
