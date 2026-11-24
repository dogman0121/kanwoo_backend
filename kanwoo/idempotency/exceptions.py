from kanwoo.exceptions import ApiBadRequest

class IdempotencyError(ApiBadRequest):
    pass