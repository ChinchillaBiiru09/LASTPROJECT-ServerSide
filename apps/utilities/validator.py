from .queries import *
from .dbHelper import DBHelper
from .utils import sanitize_email_char, sanitize_all_char, sanitize_passwd_char

import re, hashlib


def string_checker(strings):
    error = True
    if all(chr.isalpha() or chr.isspace() for chr in strings):
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
    print("hash", _hashedText)
    print("pass", hashlib.sha256(salt.encode() + password.encode()).hexdigest())
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

def vld_user_regis(name, email, password, repassword):
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

    query = USR_CHK_EMAIL_QUERY
    values = (email,)
    result = DBHelper().get_data(query, values)
    if len(result) != 0:
        checkResult.append(f"Email sudah terdaftar.")

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
# ACCOUNT VALIDATION ============================================================ End

# ROLE VALIDATION ============================================================ Begin
def vld_role(role):
    access = False

    if role.uppercase() == "ADMIN":
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