from .utils import sanitize_email_char, sanitize_all_char, sanitize_passwd_char, random_number, saving_file
from .validator import string_checker

from flask import request, current_app as app
from werkzeug.utils import secure_filename

import time, os, datetime


# TEMPLATE DATA WEDDING ============================================================ Begin
def inv_wedding(personalData, randomNumber):
    checkResult = []
    
    # Request Data ---------------------------------------- Start
    reqPersonData = ["mans_name", "mans_mom", "mans_dad", "womans_name", "womans_mom", "womans_dad", "photo_1", "photo_2", "start_date", "start_time", "end_date", "end_time", "location"]
    for data in reqPersonData:
        if data not in personalData:
            return checkResult.append(f"Gagal menyimpan undangan! Silahkan lengkapi data {data}."), personalData
    # Request Data ---------------------------------------- Finish

    
    # Initialize Request Data ---------------------------------------- Start
    manName = personalData["mans_name"].title()
    manMom = personalData["mans_mom"].title()
    manDad = personalData["mans_dad"].title()
    womanName = personalData["womans_name"].title()
    womanMom = personalData["womans_mom"].title()
    womanDad = personalData["womans_dad"].title()
    photo1 = personalData["photo_1"]
    photo2 = personalData["photo_2"]
    startDate = personalData["start_date"]
    startTime = personalData["start_time"]
    endDate = personalData["end_date"]
    endTime = personalData["end_time"]
    location = personalData["location"]
    # Initialize Request Data ---------------------------------------- Finish

    # Validation Null Data ---------------------------------------- Start
    if manName == "":
        checkResult.append(f"Nama mempelai pria tidak boleh kosong.")
    if manMom == "":
        checkResult.append(f"Nama ibu mempelai pria tidak boleh kosong.")
    if manDad == "":
        checkResult.append(f"Nama ayah mempelai pria tidak boleh kosong.")
    if womanName == "":
        checkResult.append(f"Nama mempelai wanita tidak boleh kosong.")
    if womanMom == "":
        checkResult.append(f"Nama ibu mempelai wanita tidak boleh kosong.")
    if womanDad == "":
        checkResult.append(f"Nama ayah mempelai wanita tidak boleh kosong.")
    if startDate == "":
        checkResult.append(f"Tanggal pelaksanaan tidak boleh kosong.")
    if startTime == "":
        checkResult.append(f"Waktu pelaksanaan tidak boleh kosong.")
    if location == "":
        checkResult.append(f"Lokasi pelaksanaan tidak boleh kosong.")
    # Validation Null Data ---------------------------------------- Finish
    
    # Sanitize Character ---------------------------------------- Start
    sanitMansName, charMansName = sanitize_all_char(manName)
    if sanitMansName:
        checkResult.append(f"Nama mempelai pria tidak boleh mengandung karakter {charMansName}")
    sanitMansMom, charMansMom = sanitize_all_char(manMom)
    if sanitMansMom:
        checkResult.append(f"Nama ibu mempelai pria tidak boleh mengandung karakter {charMansMom}")
    sanitMansDad, charMansDad = sanitize_all_char(manDad)
    if sanitMansDad:
        checkResult.append(f"Nama ayah mempelai pria tidak boleh mengandung karakter {charMansDad}")
    sanitWomansName, charWomansName = sanitize_all_char(womanName)
    if sanitWomansName:
        checkResult.append(f"Nama mempelai wanita tidak boleh mengandung karakter {charWomansName}")
    sanitWomansMom, charWomansMom = sanitize_all_char(womanMom)
    if sanitWomansMom:
        checkResult.append(f"Nama ibu mempelai wanita tidak boleh mengandung karakter {charWomansMom}")
    sanitWomansDad, charWomansDad = sanitize_all_char(womanDad)
    if sanitWomansDad:
        checkResult.append(f"Nama ayah mempelai wanita tidak boleh mengandung karakter {charWomansDad}")
    # Sanitize Character ---------------------------------------- Finish
    
    # String Filter ---------------------------------------- Start
    if string_checker(manName):
        checkResult.append(f"Nama mempelai pria tidak valid.")
    if string_checker(manMom):
        checkResult.append(f"Nama ibu mempelai pria tidak valid.")
    if string_checker(manDad):
        checkResult.append(f"Nama ayah mempelai pria tidak valid.")
    if string_checker(womanName):
        checkResult.append(f"Nama mempelai wanita tidak valid.")
    if string_checker(womanMom):
        checkResult.append(f"Nama ibu mempelai wanita tidak valid.")
    if string_checker(womanDad):
        checkResult.append(f"Nama ayah mempelai wanita tidak valid.")
    # String Filter ---------------------------------------- Finish

    # Saving File ---------------------------------------- Start
    # Photo1
    photo1FileName = secure_filename(time.strftime("%Y-%m-%d %H:%M:%S")+"_"+randomNumber+"_photo1.jpg")
    photo1Path = os.path.join(app.config['USER_INVITATION_FILE'], photo1FileName)
    saving_file(photo1, photo1Path)
    # Photo2
    photo2FileName = secure_filename(time.strftime("%Y-%m-%d %H:%M:%S")+"_"+randomNumber+"_photo2.jpg")
    photo2Path = os.path.join(app.config['USER_INVITATION_FILE'], photo2FileName)
    saving_file(photo2, photo2Path)
    # Saving File ---------------------------------------- Finish

    # Convert Time ---------------------------------------- Start
    personalData["start_date"] = int(datetime.datetime.timestamp(startDate)*1000)
    personalData["start_time"] = int(datetime.datetime.timestamp(startTime)*1000)
    personalData["end_date"] = int(datetime.datetime.timestamp(endDate)*1000)
    personalData["end_time"] = int(datetime.datetime.timestamp(endTime)*1000)
    # Convert Time ---------------------------------------- Finish

    # Return Value ========================================
    return checkResult, personalData
# TEMPLATE DATA WEDDING ============================================================ End

# TEMPLATE DATA BIRTHDAY ============================================================ Begin
def inv_birthday(personalData, randomNumber):
    checkResult = []
    
    # Request Data ---------------------------------------- Start
    reqPersonData = ["name", "start_date", "start_time", "end_date", "end_time", "location_party"]
    for data in reqPersonData:
        if data not in personalData:
            return checkResult.append(f"Gagal menyimpan undangan! Silahkan lengkapi data {data}."), personalData
    # Request Data ---------------------------------------- Finish

    
    # Initialize Request Data ---------------------------------------- Start
    manName = personalData["mans_name"].title()
    manMom = personalData["mans_mom"].title()
    manDad = personalData["mans_dad"].title()
    womanName = personalData["womans_name"].title()
    womanMom = personalData["womans_mom"].title()
    womanDad = personalData["womans_dad"].title()
    photo1 = personalData["photo_1"]
    photo2 = personalData["photo_2"]
    startDate = personalData["start_date"]
    startTime = personalData["start_time"]
    endDate = personalData["end_date"]
    endTime = personalData["end_time"]
    location = personalData["location"]
    # Initialize Request Data ---------------------------------------- Finish

    # Validation Null Data ---------------------------------------- Start
    if manName == "":
        checkResult.append(f"Nama mempelai pria tidak boleh kosong.")
    if manMom == "":
        checkResult.append(f"Nama ibu mempelai pria tidak boleh kosong.")
    if manDad == "":
        checkResult.append(f"Nama ayah mempelai pria tidak boleh kosong.")
    if womanName == "":
        checkResult.append(f"Nama mempelai wanita tidak boleh kosong.")
    if womanMom == "":
        checkResult.append(f"Nama ibu mempelai wanita tidak boleh kosong.")
    if womanDad == "":
        checkResult.append(f"Nama ayah mempelai wanita tidak boleh kosong.")
    if startDate == "":
        checkResult.append(f"Tanggal pelaksanaan tidak boleh kosong.")
    if startTime == "":
        checkResult.append(f"Waktu pelaksanaan tidak boleh kosong.")
    if location == "":
        checkResult.append(f"Lokasi pelaksanaan tidak boleh kosong.")
    # Validation Null Data ---------------------------------------- Finish
    
    # Sanitize Character ---------------------------------------- Start
    sanitMansName, charMansName = sanitize_all_char(manName)
    if sanitMansName:
        checkResult.append(f"Nama mempelai pria tidak boleh mengandung karakter {charMansName}")
    sanitMansMom, charMansMom = sanitize_all_char(manMom)
    if sanitMansMom:
        checkResult.append(f"Nama ibu mempelai pria tidak boleh mengandung karakter {charMansMom}")
    sanitMansDad, charMansDad = sanitize_all_char(manDad)
    if sanitMansDad:
        checkResult.append(f"Nama ayah mempelai pria tidak boleh mengandung karakter {charMansDad}")
    sanitWomansName, charWomansName = sanitize_all_char(womanName)
    if sanitWomansName:
        checkResult.append(f"Nama mempelai wanita tidak boleh mengandung karakter {charWomansName}")
    sanitWomansMom, charWomansMom = sanitize_all_char(womanMom)
    if sanitWomansMom:
        checkResult.append(f"Nama ibu mempelai wanita tidak boleh mengandung karakter {charWomansMom}")
    sanitWomansDad, charWomansDad = sanitize_all_char(womanDad)
    if sanitWomansDad:
        checkResult.append(f"Nama ayah mempelai wanita tidak boleh mengandung karakter {charWomansDad}")
    # Sanitize Character ---------------------------------------- Finish
    
    # String Filter ---------------------------------------- Start
    if string_checker(manName):
        checkResult.append(f"Nama mempelai pria tidak valid.")
    if string_checker(manMom):
        checkResult.append(f"Nama ibu mempelai pria tidak valid.")
    if string_checker(manDad):
        checkResult.append(f"Nama ayah mempelai pria tidak valid.")
    if string_checker(womanName):
        checkResult.append(f"Nama mempelai wanita tidak valid.")
    if string_checker(womanMom):
        checkResult.append(f"Nama ibu mempelai wanita tidak valid.")
    if string_checker(womanDad):
        checkResult.append(f"Nama ayah mempelai wanita tidak valid.")
    # String Filter ---------------------------------------- Finish

    # Saving File ---------------------------------------- Start
    # Photo1
    photo1FileName = secure_filename(time.strftime("%Y-%m-%d %H:%M:%S")+"_"+randomNumber+"_photo1.jpg")
    photo1Path = os.path.join(app.config['USER_INVITATION_FILE'], photo1FileName)
    saving_file(photo1, photo1Path)
    # Photo2
    photo2FileName = secure_filename(time.strftime("%Y-%m-%d %H:%M:%S")+"_"+randomNumber+"_photo2.jpg")
    photo2Path = os.path.join(app.config['USER_INVITATION_FILE'], photo2FileName)
    saving_file(photo2, photo2Path)
    # Saving File ---------------------------------------- Finish

    personalData["end_date"] = int(datetime.datetime.timestamp(endDate)*1000)
    personalData["end_time"] = int(datetime.datetime.timestamp(endTime)*1000)

    # Return Value ========================================
    return checkResult, personalData
# TEMPLATE DATA BIRTHDAY ============================================================ End
