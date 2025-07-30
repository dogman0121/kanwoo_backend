from abc import ABC, abstractmethod

class AuthMail(ABC):
    @abstractmethod
    def send_password_recovery_message(self, user_email: str, recovery_code: str):
        pass

    @abstractmethod
    def send_registration_message(self, user_email: str, registration_code: str):
        pass
