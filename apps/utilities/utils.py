import string, random
import hashlib, uuid
import cv2, base64, numpy as np


def saving_file(encodedData, fileName):
    encodedData = encodedData.split(',')[1]
    arr = np.fromstring(base64.b64decode(encodedData), np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)
    return cv2.imwrite(fileName, img)

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