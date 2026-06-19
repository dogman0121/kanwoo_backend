from kanwoo.manga.dto import NameTranslationDTO

from .schemas import AdminMangaCreateSchema, AdminMangaUpdateSchema
from .dto import AdminMangaCreateDTO, AdminMangaUpdateDTO

def _convert_name_translations_schema_into_dto(name_translations_schema):
    name_translations = []
    for translation_schema in name_translations_schema:
        t = NameTranslationDTO(
            lang_id=translation_schema.get("lang"),
            name=translation_schema.get("name")
        )
        name_translations.append(t)

    return name_translations

def _convert_manga_create_form_into_dict(form, files):
    return {
        "slug": form.get("slug"),
        "name": form.get("name"),
        "description": form.get("description"),
        "type": form.get("type", 1),
        "status": form.get("status", 1),
        "adult": form.get("adult", 0),
        "genres": form.getlist("genre", int),
        "year": form.get("year"),
        "background": files.get("background"),
        "poster": files.get("poster"),
        "name_translations": form.get("name_translations", "[]"),
        "promo_name": files.get("promo_name"),
        "promo_logo": files.get("promo_logo"),
        "promo_background": files.get("promo_background"),
        "privacy": form.get("privacy")
    }

def _convert_manga_create_schema_into_dto(schema):
    name_translations = _convert_name_translations_schema_into_dto(schema.get("name_translations"))

    return AdminMangaCreateDTO(
        name = schema.get("name"),
        slug = schema.get("slug"),
        description = schema.get("description"),
        type_id = schema.get("type"),
        status_id = schema.get("status"),
        adult_id = schema.get("adult"),
        year = schema.get("year"),
        genres_ids = schema.get("genres"),
        privacy_id= schema.get("privacy"),
        name_translations = name_translations,
        poster = schema.get("poster"),
        background = schema.get("background"),
        promo_name = schema.get("promo_name"),
        promo_logo = schema.get("promo_logo"),
        promo_background = schema.get("promo_background")
    )

def _convert_manga_update_form_into_dict(form, files):
    return {
        "slug": form.get("slug"),
        "name": form.get("name"),
        "description": form.get("description"),
        "type": form.get("type", 1),
        "status": form.get("status", 1),
        "adult": form.get("adult", 0),
        "genres": form.getlist("genre", []),
        "year": form.get("year"),
        "background": files.get("background"),
        "poster": files.get("poster"),
        "name_translations": form.get("name_translations", "[]"),
        "promo_name": files.get("promo_name"),
        "promo_logo": files.get("promo_logo"),
        "promo_background": files.get("promo_background"),
        "privacy": form.get("privacy"),
        "poster_action": form.get("poster_action"),
        "background_action": form.get("background_action"),
        "promo_name_action": form.get("promo_name_action"),
        "promo_logo_action": form.get("promo_logo_action"),
        "promo_background_action": form.get("promo_background_action")
    }

def _convert_manga_update_schema_into_dto(schema):
    name_translations = _convert_name_translations_schema_into_dto(schema.get("name_translations"))

    return AdminMangaUpdateDTO(
        name = schema.get("name"),
        slug = schema.get("slug"),
        description = schema.get("description"),
        type_id = schema.get("type"),
        status_id = schema.get("status"),
        adult_id = schema.get("adult"),
        year = schema.get("year"),
        genres_ids = schema.get("genres"),
        privacy_id= schema.get("privacy"),
        name_translations = name_translations,
        poster = schema.get("poster"),
        background = schema.get("background"),
        promo_name = schema.get("promo_name"),
        promo_logo = schema.get("promo_logo"),
        promo_background = schema.get("promo_background"),
        author_id=schema.get("author"),
        poster_action =schema.get("poster_action"),
        background_action=schema.get("background_action"),
        promo_name_action=schema.get("promo_name_action"),
        promo_logo_action=schema.get("promo_logo_action"),
        promo_background_action=schema.get("promo_background_action")
    )

def convert_manga_create_form_into_create_dto(form, files):
    create_dict = _convert_manga_create_form_into_dict(form, files)

    create_schema = AdminMangaCreateSchema().load(create_dict)

    create_dto = _convert_manga_create_schema_into_dto(create_schema)

    return create_dto

def convert_manga_update_form_into_update_dto(form, files):
    update_dict = _convert_manga_update_form_into_dict(form, files)

    update_schema = AdminMangaUpdateSchema().load(update_dict)

    update_dto = _convert_manga_update_schema_into_dto(update_schema)

    return update_dto