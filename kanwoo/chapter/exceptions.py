from kanwoo.exceptions import ApiBadRequest, ApiNotFound, ApiForbidden

class ChapterNotFoundException(ApiNotFound):
    pass

class ChapterWithNumberAlreadyExists(ApiBadRequest):
    error="chapter_already_exists"

class ChapterUpdateNotAllowed(ApiForbidden):
    pass

class ChapterDeleteNotAllowed(ApiForbidden):
    pass