from flask import request
from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required
from kanwoo.profile.services import ProfileService
from kanwoo.manga.services import MangaService
from kanwoo.manga.dto import CreateMangaDTO
from kanwoo.studio.schemas import CreateStudioMangaSchema, GetStudioMangaSchema

@profile_required()
@inject
def create_manga_handler(
    current_profile, 
    profile_slug,
    manga_service: MangaService = Provide[AppContainer.manga_container.manga_service],
    profile_service: ProfileService = Provide[AppContainer.profile_container.profile_service]
):
    create_data = CreateStudioMangaSchema().load({
        "name": request.form.get("name"),
        "privacy_id": request.form.get("privacy_id"),
        "description": request.form.get("description"),
        "type_id": request.form.get("type_id", 0),
        "status_id": request.form.get("status_id", 0),
        "adult_id": request.form.get("adult_id", 0),
        "genres_ids": request.form.getlist("genre_ids", int),
        "year": request.form.get("year"),
        "background": request.files.get("background"),
        "poster": request.files.get("poster")
    })

    create_dto = CreateMangaDTO(
        name = create_data.get("name"),
        description = create_data.get("description"),
        type_id = create_data.get("type_id"),
        status_id = create_data.get("status_id"),
        adult_id = create_data.get("adult_id"),
        year = create_data.get("year"),
        genres_ids = create_data.get("genres_ids"),
        privacy_id= create_data.get("privacy_id"),
        poster = create_data.get("poster"),
        background = create_data.get("background"),
    )

    author = profile_service.user_get_profile_by_slug(current_profile, profile_slug)

    manga = manga_service.user_create_manga(current_profile, author, create_dto) 

    manga_schema = GetStudioMangaSchema()

    return respond(data=manga_schema.dump(manga))