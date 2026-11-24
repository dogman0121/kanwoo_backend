from flask import request, Blueprint
from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer, respond
from kanwoo.middleware import pagination
from kanwoo.admin.middleware import moderator_required
from kanwoo.admin.services import AdminMangaService
from kanwoo.admin.dto import AdminMangaFiltersDTO
from kanwoo.admin.schemas import GetAdminMangaSchema

@moderator_required
@pagination
@inject
def get_manga_list_handler(
    current_profile,
    admin_manga_service: AdminMangaService = Provide[AppContainer.admin_container.admin_manga_service],
    page=1,
    per_page=20
):
    filters_dto = AdminMangaFiltersDTO(
        query=request.args.get("query", None, type=str),
        statuses=request.args.getlist("status")
    )

    manga, total_count = admin_manga_service.get_manga_list(current_profile, filters_dto, page, per_page)

    return respond(
        data=GetAdminMangaSchema().dump(manga, many=True), 
        page=page, 
        total_count=total_count, 
        per_page=per_page
    )