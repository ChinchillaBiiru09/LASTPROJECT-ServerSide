from ..confgure import config
import mysql.connector


# DBFunction Connection
def connection(host=config.DB_HOST, user=config.DB_USER, password=config.DB_PWD, database=config.DB_NAME):
    db = mysql.connector.connect(
        host=host, user=user, password=password, database=database
    )
    return db

# Select All Data to JSON
def select(conn, query, values):
    cursor = conn.cursor()
    cursor.execute(query, values)
    row_headers = [x[0] for x in cursor.description]
    results = cursor.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    return json_data

# Insert Data
def insert(conn, query, values):
    cursor = conn.cursor()
    cursor.execute(query, values)
    conn.commit()

# Insert Data Return
def insert_return(conn, query, values):
    cursor = conn.cursor()
    cursor.execute(query, values)
    conn.commit()
    return cursor.lastrowid

# Execute Query without Values
def execute(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# Row Count Data
def row_count(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    cursor.fetchall()
    rc = cursor.rowcount
    return rc

# Row Count Data with Values
def row_count_value(conn, query, values):
    cursor = conn.cursor()
    cursor.execute(query, values)
    cursor.fetchall()
    rc = cursor.rowcount
    return rc


class DBHelper():
    def __init__(self):
        self.db = connection()
    
    def get_data(self, query, values):
        return select(self.db, query, values)
    
    def get_count_data(self, query):
        return row_count(self.db, query)
    
    def get_count_filter_data(self, query, values):
        return row_count_value(self.db, query, values)
    
    def save_data(self, query, values):
        return insert(self.db, query, values)
    
    def save_return(self, query, values):
        return insert_return(self.db, query, values)

    def update_data(self, query, values):
        return insert(self.db, query, values)
    
    def execute(self, query):
        return execute(self.db, query)