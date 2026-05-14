from kanwoo.exceptions import ApiNotFound, ApiForbidden, ApiBadRequest

class MangaNotFoundException(ApiNotFound):
    pass

class MangaSaveImageException(Exception):
    pass

class MangaUpdateNotAllowedException(ApiForbidden):
    pass

class MangaDeleteNotAllowedException(ApiForbidden):
    pass

class MangaCreateTranslationNotAllowed(ApiForbidden):
    pass

class MangaInvalidData(ApiBadRequest):
    pass