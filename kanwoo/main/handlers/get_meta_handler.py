from dependency_injector.wiring import inject, Provide

from kanwoo import AppContainer, respond
from kanwoo.main.services import MetaService
from kanwoo.main.schemas import MetaSchema

@inject
def get_meta_handler(
    meta_service: MetaService = Provide[AppContainer.main_container.meta_service]
):
    meta = meta_service.get_meta()

    return respond(data=MetaSchema().dump(meta))