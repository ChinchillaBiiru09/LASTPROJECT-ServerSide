import string, random, base64, datetime
import re, time

def random_string(length):
    lowers = string.ascii_lowercase
    uppers = string.ascii_uppercase
    letters = ''.join(random.choice(lowers+uppers) for i in range(length))
    return letters

def random_number(length):
    number = string.digits
    numbers = ''.join(random.choice(number) for i in range(length))
    return numbers

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
        "--","-", "*", "%", "+", "/", "'", 
        "$", "&", "`", ".", ",", '"', ";", ":",
        "?", "^", "=", "~"
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