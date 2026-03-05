from kanwoo.exceptions import ApiBadRequest

class AuthLoginAlreadyTakenException(Exception):
    pass

class AuthEmailAlreadyTakenException(Exception):
    pass

class AuthUserWithLoginNotExistException(Exception):
    pass

class AuthPasswordNotMatchException(Exception):
    pass

class AuthJWTTokenExpiredException(Exception):
    pass

class AuthJWTTokenInvalidException(Exception):
    pass

class AuthUserWithEmailNotExistException(Exception):
    pass
