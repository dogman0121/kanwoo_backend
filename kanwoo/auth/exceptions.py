from kanwoo.exceptions import ApiBadRequest

class AuthLoginAlreadyTakenException(Exception):
    pass

class AuthEmailAlreadyTakenException(ApiBadRequest):
    pass

class AuthUserWithLoginNotExistException(Exception):
    pass

class AuthPasswordNotMatchException(ApiBadRequest):
    pass

class AuthJWTTokenExpiredException(Exception):
    pass

class AuthJWTTokenInvalidException(Exception):
    pass

class AuthUserWithEmailNotExistException(Exception):
    pass

class AuthVerificationCodeExpiredException(Exception):
    pass

class AuthWrongVerificationCodeException(ApiBadRequest):
    pass

class VerificationCodeExpiredException(Exception):
    pass