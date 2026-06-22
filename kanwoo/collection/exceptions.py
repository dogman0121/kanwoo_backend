from kanwoo.exceptions import ApiNotFound, ApiForbidden

class CollectionNotFoundException(ApiNotFound):
    error = "collection_not_found"

class CollectionUpdateNotAllowedException(ApiForbidden):
    error = "update_not_allowed"

class CollectionDeleteNotAllowedException(ApiForbidden):
    error = "delete_not_allowed"

class CollectionMangaNotExistsException(ApiNotFound):
    error = "manga_not_found"