from uuid import uuid4

class UUIDGenerator:
    @staticmethod
    def generate_uuid_v4():
        return str(uuid4())