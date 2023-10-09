from .queries import *
from .dbHelper import DBHelper
from .utils import sanitize_email_char, sanitize_all_char, sanitize_passwd_char

import re, hashlib


def string_checker(strings):
    error = True
    if all(chr.isalpha() or chr.isspace() for chr in strings):
        error = False
    return error

def phone_checker(numbers):
    error = True
    if len(numbers) > 5 and len(numbers) <= 16 and all(chr.isdigit() for chr in (numbers)):
        error = False
    return error

def email_checker(email):
    error = False
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not (re.fullmatch(regex, email)):
        error = True
        return error
    return error

def password_checker(password):
    error = False
    message= ""
    # special_chr = [",", "'", '"', "`"]
    if len(password) < 8:
        error = True
        message += "Panjang Password setidaknya harus 8."
    if len(password) > 20:
        error = True
        message += "Panjang Password tidak boleh lebih dari 20."
    if not any(char.isdigit() for char in password):
        error = True
        message += "Password harus memiliki setidaknya satu angka."
    if not any(char.isupper() for char in password):
        error = True
        message += "Password harus memiliki setidaknya satu huruf besar."  
    if not any(char.islower() for char in password):
        error = True
        message += "Password harus memiliki setidaknya satu huruf kecil."
    return error, message

def password_compare(hashedText, password):
    """fungsi untuk komparasi password yang sudah di hash dengan password dari user"""
    _hashedText, salt = hashedText.split(':')
    return _hashedText == hashlib.sha256(salt.encode() + password.encode()).hexdigest()


##########################################################################################################


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
    if len(result) != 0 or result != None:
        checkResult.append(f"Email sudah terdaftar sebagai admin.")

    return checkResult 

def vld_user_regis(fname, lname, email, password, repassword):
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
        checkResult.append(f"Nama tidak boleh mengandung karakter {charFName}")
    sanitMail, charMail = sanitize_email_char(email)
    if sanitMail:
        checkResult.append(f"Email tidak boleh mengandung karakter {charMail}")
    sanitPass, charPass = sanitize_passwd_char(password)
    if sanitPass:
        checkResult.append(f"Password tidak boleh mengandung karakter {charPass}")
    sanitRepass, charRepass = sanitize_passwd_char(repassword)
    if sanitRepass:
        checkResult.append(f"Password tidak boleh mengandung karakter {charRepass}")
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

    # Checking Las Name - If Ready ---------------------------------------- Start
    if lname != "":
        sanitLName, charLName = sanitize_all_char(lname)
        if sanitLName:
            checkResult.append(f"Nama tidak boleh mengandung karakter {charLName}")
        if string_checker(lname):
            checkResult.append(f"Nama tidak valid.")
    # Checking Last Name - If Ready ---------------------------------------- Finish

    # Checking Email on DB ---------------------------------------- Start
    query = USR_CHK_EMAIL_QUERY
    values = (email,)
    result = DBHelper().get_data(query, values)
    if len(result) != 0:
        checkResult.append(f"Email sudah terdaftar.")
    # Checking Email on DB ---------------------------------------- Finish

    # Return Checker ======================================== 
    return checkResult 

def vld_signin(email, password):
    checkResult = []

    if email == "":
        checkResult.append(f"Email tidak boleh kosong")
    if password == "":
        checkResult.append(f"Password tidak boleh kosong")


    sanitMail, charMail = sanitize_email_char(email)
    if sanitMail:
        checkResult.append(f"Email tidak boleh mengandung karakter {charMail}")
    sanitPass, charPass = sanitize_passwd_char(password)
    if sanitPass:
        checkResult.append(f"Password tidak boleh mengandung karakter {charPass}")
    
    if email_checker(email):
        checkResult.append(f"Email tidak valid.")
    
    stts = 499
    query = ADM_CHK_EMAIL_QUERY
    values = (email,)
    result = DBHelper().get_data(query, values)
    if len(result) == 0 or result == None:
        query = USR_CHK_EMAIL_QUERY
        result = DBHelper().get_data(query, values)
        if len(result) == 0 or result == None:
            stts = 400
            checkResult.append(f"Email tidak terdaftar.")
    
    savedPassword = result[0]['password']
    validatePass = password_compare(savedPassword, password)
    if not validatePass:
        stts = 400
        checkResult.append(f"Akun tidak valid.")

    return checkResult, result, stts

def vld_edit_profile(userId, userLevel, fName, mName, lName, phone):
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

    return access, "Sorry! Access denied." 
# ROLE VALIDATION ============================================================ End

# CATEGORY VALIDATION ============================================================ Begin
def vld_category(category):
    checkResult = []

    if category == "":
        checkResult.append(f"Kategori tidak boleh kosong")
    
    # Sanitize Category ---------------------------------------- Start
    sanitCtgr, charCtgr = sanitize_all_char(category)
    if sanitCtgr:
        checkResult.append(f"Kategori tidak boleh mengandung karakter {charCtgr}")
    # Sanitize Category ---------------------------------------- Finish
    
    if string_checker(category):
        checkResult.append(f"Kategori tidak valid.")

    query = CTGR_CHK_QUERY
    values = (category,)
    result = DBHelper().get_data(query, values)
    if len(result) != 0 or result != None:
        checkResult.append(f"Kategori sudah terdaftar.")

    return checkResult, result 
# CATEGORY VALIDATION ============================================================ End

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
    
    
    query = INV_CODE_CHK_QUERY
    values = (invCode,)
    result = DBHelper().get_data(query, values)
    if len(result) != 0 or result != None:
        checkResult.append(f"Kode Undangan sudah tidak aktif.")

    return checkResult 
# GREETING VALIDATION ============================================================ End