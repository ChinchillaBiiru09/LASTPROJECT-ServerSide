# ======================================================================== 
# LOG QUERY - START ======================================================
# ======================================================================== 
LOG_ADD_QUERY = """
                    INSERT INTO log 
                    (user_id, activity)
                    VALUES (%s, %s)
                """
# ======================================================================== 
# LOG QUERY - END ========================================================
# ======================================================================== 

# ========================================================================
# ADMIN QUERY - START ====================================================
# ========================================================================
ADM_CHK_EMAIL_QUERY = """SELECT * FROM admin WHERE email=%s AND is_delete=0"""
ADM_ADD_QUERY = """
                    INSERT INTO admin 
                    (name, email, password, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s)
                """
# ======================================================================== 
# ADMIN QUERY - END ====================================================== 
# ======================================================================== 


# ======================================================================== 
# USER QUERY - START =====================================================
# ======================================================================== 
USR_CHK_EMAIL_QUERY = """SELECT * FROM user WHERE email=%s AND is_delete=0"""
USR_ADD_QUERY = """
                    INSERT INTO user 
                    (name, email, password, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s)
                """
PROF_GET_BY_ID_QUERY = """
                        SELECT * FROM profile 
                        WHERE user_id=%s AND user_level=%s AND is_delete=0
                    """
# ======================================================================== 
# USER QUERY - END =======================================================
# ======================================================================== 


# ======================================================================== 
# PROFILE QUERY - START ==================================================
# ======================================================================== 
PROF_ADD_QUERY = """
                    INSERT INTO profile 
                    (user_id, user_level, first_name, middle_name, 
                    last_name, phone, photos, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
PROF_GET_BY_ID_QUERY = """
                        SELECT * FROM profile 
                        WHERE user_id=%s AND user_level=%s AND is_delete=0
                    """
PROF_UPDATE_QUERY = """
                        UPDATE profile
                        SET first_name=%s, middle_name=%s, last_name=%s, 
                        phone=%s, photos=%s, updated_at=%s
                        WHERE user_id=%s AND user_level=%s AND is_delete=0
                    """
PROF_CHECK_QUERY = """
                       SELECT * FROM profile 
                       WHERE user_id=%s AND user_level=%s AND is_delete=0
                    """
# ======================================================================== 
# PROFILE QUERY - END ====================================================
# ======================================================================== 


# ======================================================================== 
# CATEGORY QUERY - START =================================================
# ======================================================================== 
CTGR_CHK_QUERY = """
                    SELECT * FROM category 
                    WHERE category=%s AND is_delete=0
                """
CTGR_ADD_QUERY = """
                    INSERT INTO category 
                    (category, created_at, created_by, updated_at, updated_by)
                    VALUES (%s, %s, %s, %s, %s)
                """
CTGR_UPDATE_QUERY = """
                        UPDATE category 
                        SET category=%s, updated_at=%s, updated_by=%s
                        WHERE id=%s AND is_delete=0
                    """
CTGR_DELETE_QUERY = """
                        UPDATE category 
                        SET is_delete=1, deleted_at=%s, deleted_by=%s
                        WHERE id=%s AND is_delete=0
                    """
CTGR_GET_QUERY = """
                    SELECT * FROM category 
                    WHERE is_delete=0
                """
CTGR_GET_BY_ID_QUERY = """
                            SELECT * FROM category 
                            WHERE id=%s AND is_delete=0
                        """
CTGR_GET_WITH_FILTER_QUERY = """
                            """
# ======================================================================== 
# CATEGORY QUERY - END ===================================================
# ========================================================================


# ======================================================================== 
# GUEST QUERY - START ====================================================
# ======================================================================== 
GUEST_CHK_QUERY = """
                    SELECT * FROM category 
                    WHERE category=%s AND is_delete=0
                """
GUEST_ADD_QUERY = """
                    INSERT INTO category 
                    (category, created_at, created_by, updated_at, updated_by)
                    VALUES (%s, %s, %s, %s, %s)
                """
GUEST_UPDATE_QUERY = """
                        UPDATE category 
                        SET category=%s, updated_at=%s, updated_by=%s
                        WHERE id=%s AND is_delete=0
                    """
GUEST_DELETE_QUERY = """
                        UPDATE category 
                        SET is_delete=1, deleted_at=%s, deleted_by=%s
                        WHERE id=%s AND is_delete=0
                    """
GUEST_GET_QUERY = """
                    SELECT * FROM category 
                    WHERE is_delete=0
                """
GUEST_GET_BY_ID_QUERY = """
                            SELECT * FROM category 
                            WHERE id=%s AND is_delete=0
                        """
GUEST_GET_WITH_FILTER_QUERY = """
                            """
# ======================================================================== 
# GUEST QUERY - END ======================================================
# ======================================================================== 


# ======================================================================== 
# TESTER QUERY - START ====================================================
# ======================================================================== 
TEST_ADD_QUERY = """
                    INSERT INTO test 
                    (nama, file, created_at, updated_at)
                    VALUES (%s, %s, %s, %s)
                """
TEST_GET_QUERY = """
                    SELECT * FROM test 
                    WHERE is_delete=0
                """
# ======================================================================== 
# TESTER QUERY - END ======================================================
# ======================================================================== 
