import string, random
import hashlib, uuid
import cv2, base64, numpy as np
import re, hashlib

def saving_file(encodedData, fileName):
    encodedData = encodedData.split(',')[1]
    arr = np.fromstring(base64.b64decode(encodedData), np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)
    return cv2.imwrite(fileName, img)

def random_string_number(length):
    lowers = string.ascii_lowercase
    uppers = string.ascii_uppercase
    number = string.digits
    letters = ''.join(random.choice(lowers+uppers+number) for i in range(length))
    return letters

def random_string(length):
    lowers = string.ascii_lowercase
    uppers = string.ascii_uppercase
    letters = ''.join(random.choice(lowers+uppers) for i in range(length))
    return letters

def random_number(length):
    number = string.digits
    numbers = ''.join(random.choice(number) for i in range(length))
    return numbers

def hashPassword(password):
    """fungsi untuk hashing password menggunakan salt"""
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

def sanitize_all_char(string):
    special_char = [
        "(", ")", "{", "}", "[", "]", "<", ">", 
        "--", "_", "-", "*", "%", "+", "/", "'", 
        "$", "&", "`", "#", ".", ",", '"', ";", ":",
        "!", "?", "@", "^", "=", "~"
        ]
    for i in string:
        if i in special_char:
            return True, i
    return False, ""

def sanitize_passwd_char(string):
    special_char = [
        "(", ")", "{", "}", "[", "]", "<", ">", 
         "'", "`", ".", ",", '"', ";"
    ]
    for i in string:
        if i in special_char:
            return True, i
    return False, ""

def sanitize_email_char(string):
    special_char = [
        "(", ")", "{", "}", "[", "]", "<", ">", 
        "--","-", "*", "%", "+", "/", "'", 
        "$", "&", "`", ",", '"', ";", ":",
        "?", "^", "=", "~"
    ]
    for i in string:
        if i in special_char:
            return True, i
    return False, ""

def sanitize_phone_char(number):
    special_char = [
        "{", "}", "[", "]", "<", ">", 
        "--", "*", "%", "/", "'", 
        "$", "&", "`", ",", '"', ";", ":",
        "?", "^", "=", "~"
    ]
    for i in string:
        if i in special_char:
            return True, i
    return False, ""


##########################################################################################################
# CHECKER

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
    if len(password) < 6:
        error = True
        message += "Panjang Password setidaknya harus 6 karakter."
    if len(password) > 20:
        error = True
        message += "Panjang Password tidak boleh lebih dari 20 karakter."
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


