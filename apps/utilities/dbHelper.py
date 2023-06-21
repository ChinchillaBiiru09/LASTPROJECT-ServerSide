from ..confgure import config
import mysql.connector

class Database():
    # Database Connection
    def connection(host=config.DB_HOST, user=config.DB_USER, password=config.DB_PWD, database=config.DB_NAME):
        db = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return db
    
    # Select All Data to JSON
    def select(query, values, conn):
        cursor = conn.cursor()
        cursor.execute(query, values)
        row_headers = [x[0] for x in cursor.description]
        results = cursor.fetchall()
        json_data = []
        for result in results:
            json_data.append(dict(zip(row_headers, result)))
        return json_data
    
    # Insert Data
    def insert(query, values, conn):
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()

    # Insert Data Return
    def insert_return(query, values, conn):
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        return cursor.lastrowid
    
    # Execute Query without Values
    def execute(query, conn):
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall
    
    # Row Count Data
    def row_count(query, conn):
        cursor = conn.cursor()
        cursor.execute(query)
        cursor.fetchall()
        rc = cursor.rowcount
        return rc
    
    # Row Count Data with Values
    def row_count_value(query, values, conn):
        cursor = conn.cursor()
        cursor.execute(query, values)
        cursor.fetchall()
        rc = cursor.rowcount
        return rc
    
class DBHelper():
    def __init__(self):
        self.db = Database().connection()
    
    def get_data(query, values, self):
        return Database().select(query, values, self.db)
    
    def get_count_data(query, self):
        return Database().row_count(query, self.db)
    
    def get_count_filter_data(query, values, self):
        return Database().row_count_value(query, values, self.db)
    
    def save_data(query, values, self):
        return Database().insert(query, values, self.db)
    
    def save_return(query, values, self):
        return Database().insert_return(query, values, self.db)

    def update_data(query, values, self):
        return Database().insert(query, values, self.db)
    
    def execute(query, self):
        return Database().execute(query, self.db)