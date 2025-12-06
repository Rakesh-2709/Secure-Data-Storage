# data_processor.py
import hashlib

class DataProcessor:
    @staticmethod
    def calculate_data_hash(data):
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    @staticmethod
    def validate_input(label, data):
        if not label or not data:
            return False, "Label and data fields cannot be empty."
        if len(label) > 255:
            return False, "Label is too long (max 255 characters)."
        return True, ""