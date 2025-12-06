# secure_storage.py
from db_manager import DBManager
from data_processor import DataProcessor

class SecureStorageSystem:
    def __init__(self):
        self.db = DBManager()
        if not self.db.connection:
            print("System could not start. Please check MySQL configuration.")
            exit()
        print("Secure Data Storage System Initialized.")

    def store_data(self):
        print("\n--- Store New Data ---")
        label = input("Enter data label: ")
        data = input("Enter the data to secure: ")

        valid, msg = DataProcessor.validate_input(label, data)
        if not valid:
            print(f"Validation failed: {msg}")
            return

        data_hash = DataProcessor.calculate_data_hash(data)
        result = self.db.insert_record(label, data_hash, data)

        if result is True:
            print(f"✅ Data stored successfully with hash: {data_hash}")
        elif result == "DUPLICATE":
            print("⚠️ **Duplication Detected:** This data already exists.")
        else:
            print("❌ Failed to store data.")

    def retrieve_data(self):
        print("\n--- Retrieve Data ---")
        data_hash = input("Enter the data hash (SHA-256) to retrieve: ")

        if len(data_hash) != 64:
            print("❌ Invalid hash format.")
            return

        record = self.db.get_record_by_hash(data_hash)

        if record:
            label, original_data, created_at = record
            print("\n--- Record Found ---")
            print(f"Label: {label}")
            print(f"Stored On: {created_at}")
            print("-" * 20)
            print(f"Original Data: {original_data}")
            print("-" * 20)
        else:
            print(f"❌ Record not found.")

    def run(self):
        while True:
            print("\n======== SYSTEM MENU ========")
            print("1. Store Data")
            print("2. Retrieve Data")
            print("3. Exit")
            print("=============================")
            choice = input("Select an operation (1-3): ")

            if choice == '1':
                self.store_data()
            elif choice == '2':
                self.retrieve_data()
            elif choice == '3':
                self.db.close()
                break
            else:
                print("Invalid choice.")

if __name__ == "__main__":
    system = SecureStorageSystem()
    system.run()