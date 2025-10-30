import uuid

from flask import request
import json
import os
from marshmallow import ValidationError

from flask_jwt_extended import jwt_required, get_jwt_identity

from app import storage, db

from app.user.models import User
from app.profile.middleware import profile_required
from app.exceptions import ApiNotFound, ApiBadRequest, ApiForbidden
from app.entity import FileAction

from . import bp
from .models import Manga, NameTranslation, Genre, Adult, Type, Status, Poster, PosterFile
from .schemas import MangaSchema, MangaCreateSchema, MangaUpdateSchema
from .exceptions import MangaNotFoundException, MangaUpdateNotAllowedException
from .services import MangaService
from .dto import MangaCreateDTO, MangaUpdateDTO, NameTranslationDTO

from flask import abort
from app.manga.utils import get_uuid4_filename
from app.profile.middleware import profile_required

from PIL import Image

from ..logs import log_runtime
from ..utils import respond


def validate_manga():
    if not request.form.get("name"):
        return abort(respond(error="bad_request", detail={"name": "Name is empty"}, status_code=400))

    return True, ""


def update_data(manga: Manga) -> None:
    name = request.form.get("name")

    if request.form.get("name-translations") is not None:
        name_translations = json.loads(request.form.get("name-translations"))
    else:
        name_translations = {}

    description = request.form.get("description")

    type = Type.query.get(int(request.form.get("type") or 1), )
    status = Status.query.get(int(request.form.get("status") or 1), )
    year = int(request.form.get("year") or 0)

    adult = Adult.query.get(int(request.form.get("adult") or 2025), )

    genres = [Genre.get(int(i)) for i in request.form.getlist("genres")]

    authors = [User.get_by_id(int(i)) for i in request.form.getlist("authors")]
    artists = [User.get_by_id(int(i)) for i in request.form.getlist("artists")]
    publishers = [User.get_by_id(int(i)) for i in request.form.getlist("publishers")]

    manga.name = name
    manga.name_translations = [
        NameTranslation(lang=lang, name=name)
        for lang, name in name_translations.items()
    ]
    manga.description = description
    manga.type = type
    manga.status = status
    manga.year = year
    manga.adult = adult
    manga.genres = genres
    manga.authors = authors
    manga.artists = artists
    manga.publishers = publishers

poster_sizes = {
    "thumbnail": (80, 120),
    "small": (200, 300),
    "medium": (400, 600),
    "large": (600, 900),
}

def save_image(img, size, manga_id):
    ratio = img.size[0] / img.size[1]

    if ratio < 1:
        new_height = size[1]
        new_width = int(size[1] * ratio)
    else:
        new_height = int(size[0] * ratio)
        new_width = size[0]

    new_img = img.copy().convert("RGB")
    new_img.thumbnail((new_width, new_height))
    return storage.save(new_img, f"manga/{manga_id}", ext=".jpg")

background_size = (1600, 900)

def create_upload_folder(manga_id) -> None:
    if not os.path.exists(f'app/static/manga/{manga_id}'):
        os.makedirs(f'app/static/manga/{manga_id}')

def update_media(manga: Manga) -> None:
    create_upload_folder(manga.id)

    # Save posters
    if request.form.get("posters_order") is not None:
        posters_order = json.loads(request.form.get("posters_order"))
    else:
        posters_order = []

    new_posters = request.files.getlist("new_posters")

    for poster in manga.posters:
        if poster.uuid in posters_order:
            poster.order = posters_order.index(poster.uuid)
        else:
            for f in poster.files:
                storage.delete(f"/manga/{manga.id}/{f.uuid + f.ext}")
                db.session.delete(f)
            db.session.delete(poster)
            db.session.commit()

    for new_poster in new_posters:
        old_filename = new_poster.filename
        source_img = Image.open(new_poster)

        poster_uuid = str(uuid.uuid4())

        poster = Poster(
            uuid=poster_uuid,
            manga_id=manga.id,
            order=posters_order.index(old_filename)
        )

        for name, size in poster_sizes.items():
            identifier = save_image(source_img, size, manga.id)

            poster.files.append(
                PosterFile(
                    uuid=identifier,
                    ext=".jpg",
                    type=name,
                )
            )

        orig_uuid = save_image(source_img, source_img.size, manga.id)
        poster.files.append(
            PosterFile(
                uuid=orig_uuid,
                ext=".jpg",
                type="original",
            )
        )
        poster.add()

    # Save main poster
    if len(manga.posters) > 0:
        main_poster = request.form.get("main_poster")
        if main_poster in posters_order:
            manga.main_poster_number = posters_order.index(main_poster)
        else:
            manga.main_poster_number = len(manga.posters)-1

    # Save background image
    background = request.files.get("background")
    if background is not None:
        try:
            os.remove(f"app/static/manga/{manga.id}/{manga.background}")
        except FileNotFoundError:
            pass

        bg_image = Image.open(background)
        bg_image.thumbnail(background_size)

        filename = get_uuid4_filename() + ".jpg"
        bg_image.save(f"app/static/manga/{manga.id}/" + filename)
        manga.background = filename

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
        MangaService.get_manga_by_slug(slug)

        return respond(data={"available": False})
    except MangaNotFoundException:
        return respond(data={"available": True})