from kanwoo.exceptions import ApiNotFound, ApiForbidden

class CollectionNotFoundException(ApiNotFound):
    pass

class CollectionUpdateNotAllowedException(ApiForbidden):
    pass

class CollectionDeleteNotAllowedException(ApiForbidden):
    pass

class CollectionMangaNotExistsException(ApiNotFound):
    pass