from kanwoo.exceptions import ApiNotFound, ApiForbidden

class CollectionNotFoundException(ApiNotFound):
    error = "collection_not_found"

class CollectionUpdateNotAllowedException(ApiForbidden):
    error = "not_allowed"

class CollectionDeleteNotAllowedException(ApiForbidden):
    error = "not_allowed"

class CollectionMangaNotExistsException(ApiNotFound):
    error = "not_found"
