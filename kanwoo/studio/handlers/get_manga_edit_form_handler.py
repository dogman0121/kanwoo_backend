from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer, respond
from kanwoo.profile.middleware import profile_required
from kanwoo.manga.services import MangaService
from kanwoo.studio.schemas import GetStudioMangaInfoFormSchema

@profile_required()
@inject
def get_manga_edit_form_handler(
    current_profile, 
    manga_slug,
    manga_service: MangaService = Provide[AppContainer.manga_container.manga_service]
):
    manga = manga_service.user_get_manga_by_slug(current_profile, manga_slug)

    manga_data, blocked_fields = manga_service.user_get_manga_edit_form(current_profile, manga)

    return respond(
        data=GetStudioMangaInfoFormSchema(context={"blocked_fields": blocked_fields}).dump(manga_data),
    )