import mysql.connector
from mysql.connector import Error

class MySQL_Configuration:
    def __init__(self):
        self.host = "192.168.59.52"
        self.user = "usr_cobros"
        self.password = "Ti$$Xtrim2025@#cobros"
        self.database = "BD_CON_COBROS"
        self.port = 3306
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            if self.connection.is_connected():
                print("Connection to MySQL database established successfully.")
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")

    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Disconnected from MySQL database.")

    def execute_query(self, query, params=None):
        try:
            if self.connection and self.connection.is_connected():
                cursor = self.connection.cursor()
                cursor.execute(query, params)
                self.connection.commit()
                # print("Query executed successfully.")
            else:
                print("No active database connection.")
        except Error as e:
            print(f"Error while executing query: {e}")

    def fetch_results(self, query, params=None):
        try:
            if self.connection and self.connection.is_connected():
                cursor = self.connection.cursor()
                cursor.execute(query, params)
                results = cursor.fetchall()
                return results
            else:
                print("No active database connection.")
                return None
        except Error as e:
            print(f"Error while fetching results: {e}")
            return None
