from kanwoo.exceptions import ApiNotFound, ApiBadRequest, ApiForbidden

class TranslationNotFoundException(ApiNotFound):
    pass

class TranslationAlreadyExistsException(ApiBadRequest):
    error = "already_exists"

class TranslationUpdateNotAllowed(ApiForbidden):
    pass

class TranslationDeleteNotAllowed(ApiForbidden):
    pass

class TranslationChaptersForbidden(ApiForbidden):
    pass