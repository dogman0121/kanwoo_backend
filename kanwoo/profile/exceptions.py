from kanwoo.exceptions import ApiNotFound, ApiForbidden

class ProfileNotFoundException(ApiNotFound):
    pass

class ProfileUpdateNotAllowedException(ApiForbidden):
    pass

class ProfileInformationNotAllowedException(ApiForbidden):
    pass