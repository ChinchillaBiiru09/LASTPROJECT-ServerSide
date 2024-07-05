from flask import current_app as app
import string, random
import hashlib, uuid
import cv2, base64, numpy as np
import re, hashlib, os


##########################################################################################################
# FILE MANAGEMENT
def default_image():
    file_path = os.path.join(app.config['DEFAULT_PHOTOS'], "default_avatar.png")
    with open(file_path, 'rb') as file:
        blob_data = file.read()
    return blob_data

def saving_image(encodedData, fileName):
    encodedData = encodedData.split(',')[1]
    arr = np.fromstring(base64.b64decode(encodedData), np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)
    return cv2.imwrite(fileName, img)

def saving_file(encodedData, fileName):
    encodedData = encodedData.split(',')[1]
    arr = np.fromstring(base64.b64decode(encodedData), np.uint8)
    with open(fileName, "wb") as file:
        file.write(arr)


##########################################################################################################
# RANDOM CHARACTER
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


##########################################################################################################
# SANITIZING STRING
def sanitize_all_char(string):
    special_char = [
        "(", ")", "{", "}", "[", "]", "<", ">", 
        "--", "_", "-", "*", "%", "+", "/", "'", 
        "$", "&", "`", "#", ",", '"', ";", ":",
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
    for i in number:
        if i in special_char:
            return True, i
    return False, ""


##########################################################################################################
# CHECKER
def string_checker(strings):
    error = False
    for chr in strings:
        if chr.isdigit():
            error = True
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


##########################################################################################################
# TRANSFORM DATA
def password_compare(hashedText, password):
    """fungsi untuk komparasi password yang sudah di hash dengan password dari user"""
    _hashedText, salt = hashedText.split(':')
    return _hashedText == hashlib.sha256(salt.encode() + password.encode()).hexdigest()

def hashPassword(password):
    """fungsi untuk hashing password menggunakan salt"""
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

def split_date_time(datetimes):
    # Menyimpan Hari dan Bulan yang Sudah Di Format dan Diubah Ke Bahasa Indonesia
    dayFormat = ""
    monthFormat = ""
    
    # List Hari dan Bulan Dalam Bahasa Inggris dan Indonesia
    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    bln = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    # Ambil Hari dan Bulan dari Data yang datetime yang Akan di Format
    dayData = datetimes.strftime("%A")
    dateData = datetimes.strftime("%d")
    monthData = datetimes.strftime("%B")
    nummonthData = datetimes.strftime("%m")
    yearData = datetimes.strftime("%Y")
    timeData = datetimes.strftime("%H:%M")
    hourData = datetimes.strftime("%H")
    minuteData = datetimes.strftime("%M")
    partTime = datetimes.strftime("%p")
    
    # Ubah Hari dan Bulan ke Bahasa Indonesia
    for day in days:
        if day == dayData:
            dayFormat = hari[days.index(day)]
    for month in months:
        if month == monthData:
            monthFormat = bln[months.index(month)]
            fullmonthFormat = bulan[months.index(month)]
    
    # Format datetime
    datetimes = {
        "minute" : minuteData,
        "hour" : hourData,
        "day" : dayFormat,
        "dates" : dateData,
        "month" : monthFormat,
        "fullmonth" : fullmonthFormat,
        "no_month" : nummonthData,
        "year" : yearData,
        "time" : timeData,
        "day_month" : datetimes.strftime(f"%d {monthFormat}"),
        "month_year" : datetimes.strftime(f"{monthFormat} %Y"),
        "date" : datetimes.strftime(f"%d {monthFormat} %Y"),
        "date_time" : datetimes.strftime(f"%d {monthFormat} %Y %H:%M %p"),
        "edate_time" : datetimes.strftime(f"%d %B %Y %H:%M %p"),
        "full" : datetimes.strftime(f"{dayFormat}, %d {monthFormat} %Y, %H:%M:%S %p")
    }
    
    return datetimes
