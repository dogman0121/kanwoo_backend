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
    manga = manga_service.user_get_manga_by_slug(current_profile, manga_slug, by_link=True)

    update_data = UpdateStudioMangaSchema().load({
        "name": request.form.get("name"),
        "slug": request.form.get("name"),
        "description": request.form.get("description"),
        "privacy_id": request.form.get("privacy_id"),
        "type_id": request.form.get("type", 0),
        "status_id": request.form.get("status", 0),
        "adult_id": request.form.get("adult", 0),
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

    name_translations_prepared = []
    for translation in update_data.get("name_translations"):
        t = NameTranslationDTO(
            lang_id=translation.get("lang"),
            name=translation.get("name")
        )
        name_translations_prepared.append(t)

    update_dto = UpdateMangaDTO(
        name = update_data.get("name"),
        slug = update_data.get("slug"),
        description = update_data.get("description"),
        type_id = update_data.get("type"),
        status_id = update_data.get("status"),
        adult_id = update_data.get("adult"),
        year = update_data.get("year"),
        genres_ids = update_data.get("genres"),
        privacy_id= update_data.get("privacy_id"),
        name_translations = name_translations_prepared,
        poster = update_data.get("poster"),
        background = update_data.get("background"),
        poster_action = update_data.get("poster_action"),
        background_action = update_data.get("background_action"),
        promo_name = update_data.get("promo_name"),
        promo_logo = update_data.get("promo_logo"),
        promo_background = update_data.get("promo_background"),
        promo_name_action = update_data.get("promo_name_action"),
        promo_logo_action = update_data.get("promo_logo_action"),
        promo_background_action = update_data.get("promo_background_action")
    )

    updated_manga = manga_service.user_update_manga(current_profile, manga, update_dto)

    return respond(data=GetStudioMangaSchema().dump(updated_manga))