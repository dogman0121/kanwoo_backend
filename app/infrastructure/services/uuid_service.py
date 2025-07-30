from uuid import uuid4

class UUIDService:
    @staticmethod
    def generate():
        return str(uuid4())