from flask import Blueprint, request
from dependency_injector.wiring import Provide, inject

from kanwoo import AppContainer
from kanwoo.utils import respond
from kanwoo.profile.middleware import profile_required

from .services import PostService
from .schemas import PostCreateSchema, PostSchema
from .dto import PostCreateDTO

bp = Blueprint('posts', __name__, url_prefix='/posts')

@bp.get("", strict_slashes=False)
@inject
def get_posts_route(
    post_service: PostService = Provide[AppContainer.post_container.post_service]
):
    raise NotImplementedError

@bp.post('', strict_slashes=False)
@profile_required()
@inject
def create_post_route(
    current_profile,
    post_service: PostService = Provide[AppContainer.post_container.post_service]
):
    text = request.form.get("text"),

    create_schema = PostCreateSchema().load({
        "text": text
    })

    create_dto = PostCreateDTO(text=create_schema.get("text"))

    post = post_service.user_create_post(current_profile, create_dto)

    return respond(data=PostSchema().dump(post))

@bp.delete('/<int:post_id>', strict_slashes=False)
@inject
def delete_post_route(
    post_id,
    post_service: PostService = Provide[AppContainer.post_container.post_service]
):
    raise NotImplementedError