from flask import request
from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer
from kanwoo.entity import FileAction
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required
from kanwoo.manga.services import MangaService
from kanwoo.manga.dto import UpdateMangaDTO, NameTranslationDTO
from kanwoo.studio.schemas import GetStudioMangaSchema, UpdateStudioMangaSchema

@profile_required()
@inject
def update_manga_handler(
    current_profile, 
    manga_slug,
    manga_service: MangaService = Provide[AppContainer.manga_container.manga_service]
):
    manga = manga_service.user_get_manga_by_slug(current_profile, manga_slug)

    update_schema = UpdateStudioMangaSchema().load({
        "name": request.form.get("name"),
        "slug": request.form.get("slug"),
        "description": request.form.get("description"),
        "privacy_id": request.form.get("privacy_id"),
        "type_id": request.form.get("type_id", 0),
        "status_id": request.form.get("status_id", 0),
        "adult_id": request.form.get("adult_id", 0),
        "genres_ids": request.form.getlist("genres_ids", int),
        "year": request.form.get("year"),
        "name_translations": request.form.get("name_translations", "[]"),
        "background": request.files.get("background"),
        "poster": request.files.get("poster"),
        "background_action": request.form.get("background_action", FileAction.KEEP),
        "poster_action": request.form.get("poster_action", FileAction.KEEP),
        "promo_name": request.files.get("promo_name"),
        "promo_logo": request.files.get("promo_logo"),
        "promo_background": request.files.get("promo_background"),
        "promo_name_action": request.form.get("promo_name_action", FileAction.KEEP),
        "promo_logo_action": request.form.get("promo_logo_action", FileAction.KEEP),
        "promo_background_action": request.form.get("promo_background_action", FileAction.KEEP)
    })

    name_translations_prepared = list(
        map(lambda translation: NameTranslationDTO(
            lang_id=translation.get('lang'),
            name=translation.get("name")
        ), update_schema.get("name_translations"))
    )

    update_dto = UpdateMangaDTO(
        name = update_schema.get("name"),
        slug = update_schema.get("slug"),
        description = update_schema.get("description"),
        type_id = update_schema.get("type_id"),
        status_id = update_schema.get("status_id"),
        adult_id = update_schema.get("adult_id"),
        year = update_schema.get("year"),
        genres_ids = update_schema.get("genres_ids"),
        privacy_id= update_schema.get("privacy_id"),
        name_translations = name_translations_prepared,
        poster = update_schema.get("poster"),
        background = update_schema.get("background"),
        poster_action = update_schema.get("poster_action"),
        background_action = update_schema.get("background_action"),
        promo_name = update_schema.get("promo_name"),
        promo_logo = update_schema.get("promo_logo"),
        promo_background = update_schema.get("promo_background"),
        promo_name_action = update_schema.get("promo_name_action"),
        promo_logo_action = update_schema.get("promo_logo_action"),
        promo_background_action = update_schema.get("promo_background_action")
    )

    print(manga)
    updated_manga = manga_service.user_update_manga(current_profile, manga, update_dto)
    print(updated_manga)

    return respond(data=GetStudioMangaSchema().dump(updated_manga))