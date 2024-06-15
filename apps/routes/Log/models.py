from datetime import datetime
from ...utilities.responseHelper import *
from ...utilities.dbHelper import DBHelper
from ...utilities.queries import *
from ...utilities.validator import vld_role
from ...utilities.utils import split_date_time


# LOG MODEL CLASS ============================================================ Begin
class LogModels():
    # GET ALL LOG ============================================================ Begin
    def view_log(user_role):
        try:
            # Set Level Access ---------------------------------------- Start
            access = vld_role(user_role)
            if not access: # Access = True -> Admin
                return authorization_error()
            # Set Level Access ---------------------------------------- Finish

            # Checking Data ---------------------------------------- Start
            query = LOG_GET_QUERY
            result = DBHelper().execute(query)
            if len(result) < 1 or result is None:
                return not_found("Data log tidak dapat ditemukan.")
            # Checking Data ---------------------------------------- Finish
            
            # Response Data ---------------------------------------- Start
            response = []
            for rsl in result:
                data = {
                    "log_id" : rsl["id"],
                    "user_id" : rsl["user_id"],
                    "user_role": "Admin" if rsl["user_level"] == 1 else "User",
                    "activity": rsl["activity"],
                    "created_at": rsl["created_at"]
                }
                response.append(data)
            # Response Data ---------------------------------------- Finish
            
            # Return Response ======================================== 
            return success_data(response)
        
        except Exception as e:
            return bad_request(str(e))
    # GET ALL LOG ============================================================ End

    # GET LOG BY USER ============================================================ Begin
    # Clear
    def view_log_by_user(user_id, user_role):
        try:
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
            
            # Grouping & Convert Datetime ---------------------------------------- Start
            response = []
            for rsl in result:
                createdAt = datetime.fromtimestamp(rsl['created_at']/1000)
                createdAt = split_date_time(createdAt)
                rsl['created_at'] = createdAt
                data = {
                    "created_MY" : createdAt["month_year"],
                    "detail" : []
                    }
                if data in response:
                    continue
                response.append(data)
            # Grouping & Convert Datetime ---------------------------------------- Finish

            # Response Data ---------------------------------------- Start
            for res in response:
                for rsl in result:
                    if rsl["created_at"]["month_year"] in res["created_MY"]:
                        data = {
                            "log_id" : rsl["id"],
                            "user_id" : rsl["user_id"],
                            "user_role": "Admin" if rsl["user_level"] == 1 else "User",
                            "activity": rsl["activity"],
                            "created_at": rsl["created_at"]
                        }
                        res["detail"].append(data)
            # Response Data ---------------------------------------- Finish

            # Return Response ======================================== 
            return success_data(response)
        
        except Exception as e:
            return bad_request(str(e))
    # GET LOG BY USER ============================================================ End
# LOG MODEL CLASS ============================================================ End