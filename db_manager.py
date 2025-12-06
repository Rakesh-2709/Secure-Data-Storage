# db_manager.py
import mysql.connector
from config import DB_CONFIG

class DBManager:
    def __init__(self):
        try:
            # Create database if it doesn't exist
            conn = mysql.connector.connect(
                host=DB_CONFIG['host'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password']
            )
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
            cursor.close()
            conn.close()

            # Connect to the specific database
            self.connection = mysql.connector.connect(**DB_CONFIG)
            self.cursor = self.connection.cursor()
            self._create_table()
        except mysql.connector.Error as err:
            print(f"Error connecting to MySQL: {err}")
            self.connection = None

    def _create_table(self):
        if not self.connection: return
        query = """
        CREATE TABLE IF NOT EXISTS secure_records (
            id INT AUTO_INCREMENT PRIMARY KEY,
            data_label VARCHAR(255) NOT NULL,
            data_hash VARCHAR(64) UNIQUE NOT NULL,
            original_data TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.cursor.execute(query)
        self.connection.commit()

    def insert_record(self, label, data_hash, data):
        if not self.connection: return False
        try:
            query = "INSERT INTO secure_records (data_label, data_hash, original_data) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (label, data_hash, data))
            self.connection.commit()
            return True
        except mysql.connector.Error as err:
            if err.errno == 1062: # Duplicate entry
                return "DUPLICATE"
            print(f"Error inserting record: {err}")
            return False

    def get_record_by_hash(self, data_hash):
        if not self.connection: return None
        query = "SELECT data_label, original_data, created_at FROM secure_records WHERE data_hash = %s"
        self.cursor.execute(query, (data_hash,))
        result = self.cursor.fetchone()
        return result

    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()