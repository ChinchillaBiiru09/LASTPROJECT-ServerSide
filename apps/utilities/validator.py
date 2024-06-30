from .queries import *
from .dbHelper import DBHelper
from .utils import *
from .templateData import *

from datetime import datetime

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
        checkResult.append(f"Password tidak boleh kosong")
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
        checkResult.append(f"Password tidak boleh mengandung simbol '{charRepass}'. Gunakan selain simbol '( ) [ ] < > ' ` \" ; . ,'.")
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
        checkResult.append("Kategori tidak boleh kosong.")
    if type(format_data) != dict:
        checkResult.append("Format data tidak valid.")
    if format_data is None or len(format_data) < 1:
        checkResult.append("Format data undangan tidak boleh kosong.")
    # Check Null Value ---------------------------------------- Finish

    # Sanitize Category ---------------------------------------- Start
    sanitCtgr, charCtgr = sanitize_all_char(category)
    if sanitCtgr:
        checkResult.append(f"Kategori tidak boleh mengandung karakter {charCtgr}.")
    # Sanitize Category ---------------------------------------- Finish
    
    # Check String Value ---------------------------------------- Start
    if string_checker(category):
        checkResult.append("Kategori tidak valid.")
    # Check String Value ---------------------------------------- Finish

    # Check Duplicate Category ---------------------------------------- Start
    mandatory = ["name_a", "date", "time", "address"]
    for default in mandatory:
        if default not in format_data:
            checkResult.append(f"Minimal tambahkan format {default}.")
    # Check Duplicate Category ---------------------------------------- Finish

    # Check Duplicate Category ---------------------------------------- Start
    if is_create:
        query = CTGR_CHK_QUERY
        values = (category,)
        result = DBHelper().get_count_filter_data(query, values)
        if result > 0:
            checkResult.append("Kategori sudah terdaftar.")
    # Check Duplicate Category ---------------------------------------- Finish

    return checkResult
# CATEGORY VALIDATION ============================================================ End

# GUEST VALIDATION ============================================================ Begin
def vld_guest(name, address, phone):
    checkResult = []

    if name == "":
        checkResult.append(f"Nama tidak boleh kosong")
    if address == "":
        checkResult.append(f"Alamat tidak boleh kosong")
    if phone == "":
        checkResult.append(f"Nomor handphone tidak boleh kosong")


    sanitName, charName = sanitize_all_char(name)
    if sanitName:
        checkResult.append(f"Nama tidak boleh mengandung karakter {charName}")
    sanitPhone, charPhone = sanitize_phone_char(phone)
    if sanitPhone:
        checkResult.append(f"Nomor handphone tidak boleh mengandung karakter {charPhone}")
        
    
    if string_checker(name):
        checkResult.append(f"Nama tidak valid")
    if phone_checker(phone):
        checkResult.append(f"Nomor handphone tidak valid")

    return checkResult 
# GUEST VALIDATION ============================================================ End

# GREETING VALIDATION ============================================================ Begin
def vld_greeting(invCode, name, email, greeting):
    checkResult = []

    if name == "":
        checkResult.append(f"Nama tidak boleh kosong")
    if email == "":
        checkResult.append(f"Email tidak boleh kosong")
    if greeting == "":
        checkResult.append(f"Pesan tidak boleh kosong")


    sanitName, charName = sanitize_all_char(name)
    if sanitName:
        checkResult.append(f"Nama tidak boleh mengandung karakter {charName}")
    sanitMail, charMail = sanitize_email_char(email)
    if sanitMail:
        checkResult.append(f"Email tidak boleh mengandung karakter {charMail}")
        
    
    if string_checker(name):
        checkResult.append(f"Nama tidak valid.")
    if email_checker(email):
        checkResult.append(f"Email tidak valid.")
    
    
    query = INV_CHK_CODE_QUERY
    values = (invCode,)
    result = DBHelper().get_data(query, values)
    if len(result) < 1:
        checkResult.append(f"Data Undangan tidak dapat ditemukan.")

    return checkResult 
# GREETING VALIDATION ============================================================ End

# TEMPLATE VALIDATION ============================================================ Begin
def vld_template(title, thumbnail, css, wallpaper):
    checkResult = []

    if title == "":
        checkResult.append(f"Judul template tidak boleh kosong")
    if thumbnail == "":
        checkResult.append(f"Thumbnail tidak boleh kosong")
    if css == "":
        checkResult.append(f"Css tidak boleh kosong")
    if wallpaper == "":
        checkResult.append(f"Wallpaper tidak boleh kosong")
    
    # Sanitize Title ---------------------------------------- Start
    sanitTitle, charTitle = sanitize_all_char(title)
    if sanitTitle:
        checkResult.append(f"Judul tidak boleh mengandung karakter {charTitle}")
    # Sanitize Title ---------------------------------------- Finish
    
    # if string_checker(title):
    #     checkResult.append(f"Judul tidak valid.")

    query = TMPLT_CHK_QUERY
    values = (title,)
    result = DBHelper().get_count_filter_data(query, values)
    if result != 0:
        checkResult.append("Judul sudah terdaftar.")

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

def vld_invitation(categoryId, templateId, title, personalData):
    checkResult = []

    # Validation Null Data ---------------------------------------- Start
    if title == "":
        checkResult.append(f"Judul template tidak boleh kosong.")
    if personalData == None:
        checkResult.append(f"Data pribadi tidak boleh kosong tidak boleh kosong.")
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
    sanitTitle, charTitle = sanitize_all_char(title)
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

    # Check Format Data ---------------------------------------- Start
    personData = True
    if len(personalData) < 1:
        personData = False
        checkResult.append("Personal data tidak boleh kosong.")
    # elif len(ckCategory) > 0:
    #     formatData = json.loads(ckCategory[0]["format_data"])
    #     for key, value in formatData.items():
    #         if value == "required" and key not in personalData:
    #             checkResult.append(f"Missing data {key} from personal data.")
    #         elif value == "required":
    #             if personalData[key] == "" or personalData[key] is None:
    #                 personData = False
    #                 checkResult.append(f"Data {key} tidak boleh kosong.")
    # Check Format Data ---------------------------------------- Finish

    # Check Personal Data ---------------------------------------- Start
    if personData:
        marriageDate = datetime.strptime(personalData["marriage"], "%d %B %Y %H:%M %p")
        receptionDate = datetime.strptime(personalData["reception"], "%d %B %Y %H:%M %p")
        marriageDate = datetime.timestamp(marriageDate)
        receptionDate = datetime.timestamp(receptionDate)
        personalData["marriage"] = int(round(marriageDate*1000))
        personalData["reception"] = int(round(receptionDate*1000))
    # Check Personal Data ---------------------------------------- Finish

    # Create Invitation Code ========================================
    invCode = vld_invitation_code()

    # Return Value ========================================
    return checkResult, personalData, invCode
# INVITATION VALIDATION ============================================================ End
