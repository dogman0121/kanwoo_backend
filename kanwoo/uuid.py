from uuid import uuid4

class UUID:
    @staticmethod
    def generate_uuid():
        return str(uuid4())