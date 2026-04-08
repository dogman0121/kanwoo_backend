class UserAlreadyExistsException(Exception):
    pass


class UserNotFoundException(Exception):
    pass


class UserLoginAlreadyTakenException(Exception):
    pass


class UserEmailAlreadyTakenException(Exception):
    pass
