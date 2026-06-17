from kanwoo.exceptions import ApiNotFound, ApiBadRequest, ApiForbidden

class TranslationNotFoundException(ApiNotFound):
    error = "translation_not_found"

class TranslationAlreadyExistsException(ApiBadRequest):
    error = "already_exists"

class TranslationUpdateNotAllowed(ApiForbidden):
    error = "update_not_allowed"

class TranslationDeleteNotAllowed(ApiForbidden):
    error = "delete_not_allowed"

class TranslationChaptersForbidden(ApiForbidden):
    pass