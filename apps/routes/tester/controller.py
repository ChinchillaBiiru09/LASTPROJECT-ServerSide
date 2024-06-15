from flask import Blueprint, request, make_response, jsonify, current_app as app
from flask_jwt_extended import jwt_required, get_jwt\


from ...utilities.dbHelper import DBHelper
from ...utilities.responseHelper import *
from ...utilities.queries import *
from ...utilities.utils import *
from ...utilities.validator import *

import base64, time


# BLUEPRINT ============================================================ Begin
test = Blueprint(
    name='test',
    import_name=__name__,
    url_prefix='/test'
)
# BLUEPRINT ============================================================ End


# TEST BLOB DATA ============================================================ Begin
# POST https://127.0.0.1:5000/user/
@test.post('/a')
def testcreateblob():
    try:
        # Request Data ======================================== 
        data = request.json

        if data == None:
                return invalid_params()
            
        requiredData = ["title", "file"]
        for req in requiredData:
            if req not in data:
                return parameter_error(f"Missing {req} in Request Body")
        
        nama = data["title"]
        file = data["file"]

        binary_data = base64.b64decode(file)
        timestamp = int(round(time.time()*1000))
        query = TEST_ADD_QUERY
        values = (nama, binary_data, timestamp, timestamp)
        DBHelper().save_data(query, values)

        return success("Berhasil:)")

    
    except Exception as e:
        return bad_request(str(e))

@test.get('/a')
def testgetblob():
    try:
        # Request Data ======================================== 
        
        query = TEST_GET_QUERY
        result = DBHelper().execute(query)

        print(TEST_GET_QUERY)
        print(result[0][2])

        base_64 = base64.b64encode(result[0][2]).decode('utf-8')
        print(base_64)
        response = {
            # "pothos" : result[0]["photos"],
            "base64" : base_64.strip()
        }

        return success_data("Berhasil:)", response)

    
    except Exception as e:
        return bad_request(str(e))
# TEST BLOB DATA ============================================================ End


# TEST LOG ON PROFILE ============================================================ Begin
# GET https://127.0.0.1:5000/test/activity
@test.post('/activity')
@jwt_required()
def create_log():
    try:
        # Access User ======================================== 
        user_id = str(get_jwt()["id"])
        user_role = str(get_jwt()["role"])

        # Set Level Access ---------------------------------------- Start
        access = vld_role(user_role) # Access = True -> Admin
        accLevel = 1 if access else 2 # 1 = Admin | 2 = User
        # Set Level Access ---------------------------------------- Finish

        # Checking Data ---------------------------------------- Start
        act = "coba contoh ku."
        timestamp = int(round(time.time()*1000))
        query = LOG_ADD_QUERY
        values = (user_id, accLevel, act, timestamp, )
        DBHelper().save_data(query, values)
        # Checking Data ---------------------------------------- Finish
        
        # Return Response ======================================== 
        return success()
    
    except Exception as e:
        return bad_request(str(e))

# GET https://127.0.0.1:5000/test/activity
@test.get('/activity')
@jwt_required()
def get_data_by_user():
    try:
        # Access User ======================================== 
        user_id = str(get_jwt()["id"])
        user_role = str(get_jwt()["role"])

        # Set Level Access ---------------------------------------- Start
        access = vld_role(user_role) # Access = True -> Admin
        accLevel = 1 if access else 2 # 1 = Admin | 2 = User
        # Set Level Access ---------------------------------------- Finish

        # Checking Data ---------------------------------------- Start
        query = LOG_GET_BY_USER_QUERY
        values = (user_id, accLevel, )
        result = DBHelper().get_data(query, values)
        if len(result) < 1 or result is None :
            return not_found(f"Data log untuk user {user_id} tidak dapat ditemukan.")
        # Checking Data ---------------------------------------- Finish
        times = str(int(round(time.time()*1000)))
        print(times)
        
        # Example ---------------------------------------- Start
        date = []
        for rsl in result:
            createdAt = datetime.datetime.fromtimestamp(rsl['created_at']/1000)
            createdAt = split_date_time(createdAt)
            data = {
                    "log_id" : rsl["id"],
                    "date" : createdAt["month_year"]
                }
            date.append(data)
            # rsl["created_at"] = createdAt
        
        test = []
        for i in date:
            coba = {
                "my" : i["date"],
                "act" : []
                }
            if coba in test:
                continue
            test.append(coba)

        for ts in test:
            for dt in date:
                if dt["date"] in ts["my"]:
                    ts["act"].append(dt)
        # Example ---------------------------------------- Finish
        
        # Grouping Data ---------------------------------------- Start
        response = [] # sementara
        for rsl in result:
            createdAt = datetime.datetime.fromtimestamp(rsl['created_at']/1000)
            createdAt = split_date_time(createdAt)
            rsl['created_at'] = createdAt
            data = {
                "created_M_Y" : createdAt["month_year"],
                "detail" : []
                }
            if data in response:
                continue
            response.append(data)
        # Grouping Data ---------------------------------------- Finish
        
        # Response Data ---------------------------------------- Start
        for res in response:
            for rsl in result:
                if rsl["created_at"]["month_year"] == res["created_M_Y"]:
                    data = {
                        "log_id" : rsl["id"],
                        "user_id" : rsl["user_id"],
                        "user_role": "Admin" if rsl["user_level"] == 1 else "User",
                        "activity": rsl["activity"],
                        "created_at": rsl["created_at"]
                    }
                    res["detail"].append(data)
        # Response Data ---------------------------------------- Finish
        print(response)

        # Return Response ======================================== 
        return success_data(response)
    
    except Exception as e:
        return bad_request(str(e))
# TEST LOG ON PROFILE ============================================================ End