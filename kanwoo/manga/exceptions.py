from kanwoo.exceptions import ApiNotFound, ApiForbidden, ApiBadRequest

class MangaNotFoundException(ApiNotFound):
    error = "manga_not_found"

class MangaSaveImageException(Exception):
    pass

class MangaCreateNotAllowedException(ApiForbidden):
    pass

class MangaUpdateNotAllowedException(ApiForbidden):
    pass

class MangaDeleteNotAllowedException(ApiForbidden):
    pass

class MangaCreateTranslationNotAllowed(ApiForbidden):
    pass

class MangaInvalidData(ApiBadRequest):
    pass