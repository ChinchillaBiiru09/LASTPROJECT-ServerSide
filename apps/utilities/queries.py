# ======================================================================== 
# LOG QUERY - START ======================================================
# ======================================================================== 
LOG_ADD_QUERY = """
                    INSERT INTO log 
                    (user_id, user_level, activity, created_at)
                    VALUES (%s, %s, %s, %s)
                """
LOG_GET_QUERY = """
                    SELECT * FROM log
                    WHERE is_delete=0
                """
LOG_GET_BY_USER_QUERY = """
                            SELECT * FROM log
                            WHERE user_id=%s AND user_level=%s AND is_delete=0
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
                    (username, email, password, last_active, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
ADM_GET_BY_ID_QUERY = """
                        SELECT * FROM admin
                        WHERE id=%s AND is_delete=0
                    """
ADM_UPDATE_ACTIVE_QUERY = """
                            UPDATE admin 
                            SET last_active=%s
                            WHERE id=%s AND is_delete=0
                        """
ADM_DELETE_QUERY = """
                        UPDATE admin 
                        SET is_delete=1, deleted_at=%s
                        WHERE id=%s AND is_delete=0
                    """
ADM_DELETE_PERMANENT_QUERY = """
                                DELETE FROM admin
                                WHERE id=%s AND is_delete=0
                            """
# ======================================================================== 
# ADMIN QUERY - END ====================================================== 
# ======================================================================== 


# ======================================================================== 
# USER QUERY - START =====================================================
# ======================================================================== 
USR_CHK_EMAIL_QUERY = """
                        SELECT * FROM user WHERE email=%s AND is_delete=0
                    """
USR_ADD_QUERY = """
                    INSERT INTO user 
                    (username, email, password, last_active, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
USR_GET_ALL_QUERY = """
                        SELECT * FROM user
                        WHERE is_delete=0
                    """
USR_GET_BY_ID_QUERY = """
                        SELECT * FROM user
                        WHERE id=%s AND is_delete=0
                    """
USR_UPDATE_ACTIVE_QUERY = """
                            UPDATE user 
                            SET last_active=%s
                            WHERE id=%s AND is_delete=0
                        """
USR_DELETE_QUERY = """
                        UPDATE user 
                        SET is_delete=1, deleted_at=%s, deleted_by=%s
                        WHERE id=%s AND is_delete=0
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
PROF_PHOTO_BY_ID_QUERY = """
                        SELECT id, user_id, user_level, photos FROM profile 
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
                    (category, format_data, created_at, created_by, updated_at, updated_by)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
CTGR_UPDATE_QUERY = """
                        UPDATE category 
                        SET category=%s, format_data=%s, updated_at=%s, updated_by=%s
                        WHERE id=%s AND is_delete=0
                    """
CTGR_DELETE_QUERY = """
                        UPDATE category 
                        SET is_delete=1, deleted_at=%s, deleted_by=%s
                        WHERE id=%s AND is_delete=0
                    """
CTGR_GET_ALL_QUERY = """
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
# GREETING QUERY - START =================================================
# ======================================================================== 
INV_CODE_CHK_QUERY = """
                    SELECT * FROM invitation 
                    WHERE invitation_code=%s AND is_delete=0
                """
GRTG_ADD_QUERY = """
                    INSERT INTO greeting 
                    (name, email, message, invitation_code, user_id, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
GRTG_GET_ALL_QUERY = """
                    SELECT * FROM greeting 
                    WHERE is_delete=0
                """
GRTG_GET_BY_ID_QUERY = """
                            SELECT * FROM greeting 
                            WHERE id=%s AND is_delete=0
                        """
GRTG_GET_BY_USER_QUERY = """
                            SELECT * FROM greeting 
                            WHERE user_id=%s AND is_delete=0
                        """
GRTG_DELETE_QUERY = """
                        UPDATE greeting 
                        SET is_delete=1, deleted_at=%s, deleted_by=%s
                        WHERE id=%s AND is_delete=0
                    """
# ======================================================================== 
# GREETING QUERY - END ===================================================
# ======================================================================== 


# ======================================================================== 
# TEMPLATE QUERY - START =================================================
# ======================================================================== 
TMPLT_CHK_QUERY = """
                    SELECT * FROM template 
                    WHERE title=%s AND is_delete=0
                """
TMPLT_ADD_QUERY = """
                    INSERT INTO template 
                    (title, thumbnail, css_file, js_file, wallpaper, category_id, created_at, created_by, updated_at, updated_by)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
TMPLT_UPDATE_QUERY = """
                        UPDATE template 
                        SET title=%s, thumbnail=%s, css_file=%s, js_file=%s, 
                        wallpaper=%s, category_id=%s, updated_at=%s, updated_by=%s
                        WHERE id=%s AND is_delete=0
                    """
TMPLT_DELETE_QUERY = """
                        UPDATE template 
                        SET is_delete=1, deleted_at=%s, deleted_by=%s
                        WHERE id=%s AND is_delete=0
                    """
TMPLT_GET_ALL_QUERY = """
                    SELECT * FROM template 
                    WHERE is_delete=0
                """
TMPLT_GET_BY_ID_QUERY = """
                            SELECT * FROM template 
                            WHERE id=%s AND is_delete=0
                        """
TMPLT_GET_WITH_FILTER_QUERY = """
                            """
# ======================================================================== 
# TEMPLATE QUERY - END ===================================================
# ========================================================================


# ======================================================================== 
# REQ TEMPLATE QUERY - START =================================================
# ======================================================================== 
TMPLT_CHK_QUERY = """
                    SELECT * FROM template 
                    WHERE title=%s AND is_delete=0
                """
REQ_ADD_QUERY = """
                    INSERT INTO requser 
                    (user_id, user_level, category, design_file, description, deadline, type, status, created_at, created_by, updated_at, updated_by)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
# ======================================================================== 
# REQ TEMPLATE QUERY - END ===================================================
# ========================================================================


# ========================================================================
# INVITATION QUERY - START ===============================================
# ========================================================================
INV_CHK_TITLE_QUERY = """
                            SELECT title FROM invitation 
                            WHERE title=%s AND is_delete=0
                        """
INV_CHK_CODE_QUERY = """
                        SELECT code FROM invitation 
                        WHERE code=%s AND is_delete=0
                    """
INV_ADD_QUERY = """
                    INSERT INTO invitation 
                    (user_level, user_id, category_id, template_id, title, wallpaper, personal_data, inv_setting, code, link, created_at, created_by, updated_at, updated_by)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
INV_UPDATE_QUERY = """
                        UPDATE invitation 
                        SET category=%s, updated_at=%s, updated_by=%s
                        WHERE id=%s AND is_delete=0
                    """
INV_DELETE_QUERY = """
                        UPDATE invitation 
                        SET is_delete=1, deleted_at=%s, deleted_by=%s
                        WHERE id=%s AND is_delete=0
                    """
INV_GET_ALL_QUERY = """
                        SELECT * FROM invitation 
                        WHERE is_delete=0
                    """
INV_GET_USER_ID_QUERY = """
                        SELECT * FROM invitation 
                        WHERE user_id=%s AND user_level=%s AND is_delete=0
                    """
INV_GET_BY_ID_QUERY = """
                        SELECT * FROM invitation 
                        WHERE id=%s AND is_delete=0
                    """
INV_GET_BY_USR_QUERY = """
                            SELECT * FROM invitation 
                            WHERE user_id=%s AND user_level=%s 
                            AND is_delete=0
                        """
INV_GET_WITH_FILTER_QUERY = """
                            """
# ========================================================================
# INVITATION QUERY - END =================================================
# ========================================================================


# ======================================================================== 
# GUEST QUERY - START ====================================================
# ======================================================================== 
GUEST_CHK_QUERY = """
                    SELECT * FROM guest 
                    WHERE category=%s AND is_delete=0
                """
GUEST_ADD_QUERY = """
                    INSERT INTO guest 
                    (category, created_at, created_by, updated_at, updated_by)
                    VALUES (%s, %s, %s, %s, %s)
                """
GUEST_UPDATE_QUERY = """
                        UPDATE guest 
                        SET category=%s, updated_at=%s, updated_by=%s
                        WHERE id=%s AND is_delete=0
                    """
GUEST_DELETE_QUERY = """
                        UPDATE guest 
                        SET is_delete=1, deleted_at=%s, deleted_by=%s
                        WHERE id=%s AND is_delete=0
                    """
GUEST_GET_ALL_QUERY = """
                        SELECT * FROM guest 
                        WHERE is_delete=0
                    """
GUEST_GET_BY_ID_QUERY = """
                            SELECT * FROM guest 
                            WHERE id=%s AND is_delete=0
                        """
GUEST_GET_BY_USR_QUERY = """
                            SELECT * FROM guest 
                            WHERE user_id=%s AND is_delete=0
                        """
GUEST_GET_WITH_FILTER_QUERY = """
                            """
GUEST_GET_GROUP_COUNT_QUERY = """
                            SELECT category_id, code, user_id, 
                            COUNT(*) as count FROM guest
                            WHERE user_id=%s AND is_delete=0
                            GROUP BY code
                        """
# ======================================================================== 
# GUEST QUERY - END ======================================================
# ======================================================================== 


# ======================================================================== 
# TESTER QUERY - START ===================================================
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
# TESTER QUERY - END =====================================================
# ========================================================================