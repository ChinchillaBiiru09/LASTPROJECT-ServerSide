from flask import Blueprint, request, make_response, jsonify, current_app as app

from ...utilities.responseHelper import invalid_params, parameter_error, defined_error, bad_request, success, success_data
from ...utilities.dbHelper import DBHelper
from ...utilities.queries import *
from ...utilities.utils import hashPassword
from ...utilities.validator import vld_user_regis, vld_signin, vld_role
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
            
        requiredData = ["nama", "file"]
        for req in requiredData:
            if req not in data:
                return parameter_error(f"Missing {req} in Request Body")
        
        nama = data["nama"]
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