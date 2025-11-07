from flask import request
from marshmallow import ValidationError

from flask import abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import storage, db

from app.profile.middleware import profile_required
from app.exceptions import ApiNotFound, ApiBadRequest, ApiForbidden
from app.entity import FileAction
from app.manga.utils import get_uuid4_filename
from app.translation.exceptions import TranslationNotFoundException
from app.translation.services import TranslationService
from app.chapter.services import ChapterService
from app.chapter.schemas import ChapterCreateSchema, ChapterSchemaMini
from app.chapter.dto import ChapterCreateDTO

from . import bp
from .schemas import MangaSchema, MangaCreateSchema, MangaUpdateSchema
from .exceptions import MangaNotFoundException, MangaUpdateNotAllowedException
from .services import MangaService
from .dto import MangaCreateDTO, MangaUpdateDTO, NameTranslationDTO


from PIL import Image

from ..logs import log_runtime
from ..utils import respond

@bp.route("", methods=["POST"], strict_slashes=False)
@profile_required()
def add_manga(profile):
    name = request.form.get("name")

    create_schema = MangaCreateSchema()
    create_data = create_schema.load({
        "name": name
    })

    create_dto = MangaCreateDTO(
        name=create_data.get("name")
    )

    manga = MangaService(profile).create_manga(create_dto)

    manga_schema = MangaSchema()

    return respond(data=manga_schema.dump(manga))
    

@bp.route('/<slug>', methods=['GET'])
@log_runtime
@profile_required(optional=True)
def get_manga_route(profile, slug):
    try:
        manga = MangaService(profile).get_manga_by_slug(slug)

        schema = MangaSchema()

        return respond(data=schema.dump(manga), status_code=200)
    except MangaNotFoundException:
        raise ApiNotFound


@bp.route("/<slug>", methods=["PUT"])
@profile_required()
def edit_manga(profile, slug):
    try:
        manga = MangaService(profile).get_manga_by_slug(slug)

        new_slug = request.form.get("slug")
        name = request.form.get("name")
        description = request.form.get("description")
        type = request.form.get("type", 0)
        status = request.form.get("status", 0)
        adult = request.form.get("adult", 0)
        genres = request.form.getlist("genre", int)
        year = request.form.get("year")
        name_translations = request.form.get("nameTranslations", "[]")
        background = request.files.get("background")
        poster = request.files.get("poster")
        background_action = request.form.get("backgroundAction", FileAction.KEEP)
        poster_action = request.form.get("posterAction", FileAction.KEEP)
        promo_name = request.files.get("promoName")
        promo_logo = request.files.get("promoLogo")
        promo_background = request.files.get("promoBackground")
        promo_name_action = request.form.get("promoNameAction", FileAction.KEEP)
        promo_logo_action = request.form.get("promoLogoAction", FileAction.KEEP)
        promo_background_action = request.form.get("promoBackgroundAction", FileAction.KEEP)

        update_schema = MangaUpdateSchema()
        update_data = update_schema.load({
            "name": name,
            "slug": new_slug,
            "description": description,
            "type": type,
            "status": status,
            "adult": adult,
            "genres": genres,
            "year": year,
            "name_translations": name_translations,
            "background": background,
            "poster": poster,
            "background_action": background_action,
            "poster_action": poster_action,
            "promo_name": promo_name,
            "promo_logo": promo_logo,
            "promo_background": promo_background,
            "promo_name_action": promo_name_action,
            "promo_logo_action": promo_logo_action,
            "promo_background_action": promo_background_action
        })

        name_translations_prepared = []
        for translation in update_data.get("name_translations"):
            t = NameTranslationDTO(
                lang=translation.get("lang"),
                name=translation.get("name")
            )
            name_translations_prepared.append(t)

        update_dto = MangaUpdateDTO(
            name = update_data.get("name"),
            slug = update_data.get("slug"),
            description = update_data.get("description"),
            type = update_data.get("type"),
            status = update_data.get("status"),
            adult = update_data.get("adult"),
            year = update_data.get("year"),
            genres = update_data.get("genres"),
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

        updated_manga = MangaService(profile).update_manga(manga, update_dto)

        manga_schema = MangaSchema()

        return respond(data=manga_schema.dump(updated_manga))
    except ValidationError as e:
        raise ApiBadRequest(detail=e.messages)
    except MangaNotFoundException:
        raise ApiNotFound
    except MangaUpdateNotAllowedException:
        raise ApiForbidden
    


@bp.route("/<slug>", methods=["DELETE"])
@jwt_required()
def delete_manga_v1(slug):
    pass

@bp.route("/<slug>/reports", methods=["POST"])
def report_manga_route(slug):
    return respond(data={"success": True})


@bp.route("/suggestions", methods=["POST"])
def suggest_manga_route():
    return respond(data={"success": True})

@bp.route("/check_slug", methods=["GET"])
def check_slug_route():
    slug = request.args.get("slug")

    try:
        MangaService().get_manga_by_slug(slug)

        return respond(data={"available": False})
    except MangaNotFoundException:
        return respond(data={"available": True})
    
@bp.route("/manga/<slug>/translations", methods=["GET"])
@profile_required(optional=True)
def get_manga_translations_route(profile, slug):
    pass
    
@bp.route("/<slug>/chapters", methods=["POST"])
@profile_required()
def add_manga_chapter_route(profile, slug):
    try:
        manga = MangaService(profile).get_manga_by_slug(slug)

        chapter_number = request.form.get("chapter", type=int)
        tome = request.form.get("tome", type=int)
        name = request.form.get("name") 
        pages_order = request.form.get("pages_order")
        pages = request.files.getlist("page")

        create_schema = ChapterCreateSchema()

        create_data = create_schema.load({
            "chapter": chapter_number,
            "tome": tome,
            "name": name,
            "pages_order": pages_order,
            "pages": pages
        })

        create_dto = ChapterCreateDTO(
            chapter=create_data.get("chapter"),
            tome=create_data.get("tome"),
            name=create_data.get("name"),
            pages_order=create_data.get("pages_order"),
            pages=create_data.get("pages"),
        )

        try:
            translation = TranslationService(profile).get_manga_translation(manga)
        except TranslationNotFoundException:
            translation = TranslationService(profile).create_manga_translation(manga)

        chapter = ChapterService(profile).create_chapter(translation, create_dto)

        schema = ChapterSchemaMini()

        return respond(schema.dump(chapter))
    except MangaNotFoundException:
        raise ApiNotFound
    


