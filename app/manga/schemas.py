from marshmallow import Schema, fields, pre_load, ValidationError

import json

from app import storage
from app.profiles.schemas import ProfileSchema


class MangaTypeSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)

class MangaStatusSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)

class MangaAdultSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)

class MangaGenreSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)

class MangaPermissionSchema(Schema):
    edit = fields.Boolean()
    delete = fields.Boolean()
    verify = fields.Boolean()

class MangaNameTranslationsSchema(Schema):
    lang = fields.String(required=True)
    name = fields.String(required=True)

class MangaPosterSchema(Schema):
    thumbnail = fields.String()
    small = fields.String()
    medium = fields.String()
    large = fields.String()
    orig = fields.String()


class MangaSchema(Schema):
    id = fields.Integer(required=True)
    slug = fields.String(required=True)
    name = fields.String(required=True)
    name_translations = fields.List(fields.Nested(MangaNameTranslationsSchema))
    description = fields.String()
    status = fields.Nested(MangaStatusSchema)
    type = fields.Nested(MangaTypeSchema)
    adult = fields.Nested(MangaAdultSchema)
    genres = fields.List(fields.Nested(MangaGenreSchema))
    year = fields.Integer()
    main_poster = fields.Nested(MangaPosterSchema)
    background = fields.Method("get_background")
    posters = fields.List(fields.Nested(MangaPosterSchema))
    authors = fields.List(fields.Nested(ProfileSchema))
    artists = fields.List(fields.Nested(ProfileSchema))
    publishers = fields.List(fields.Nested(ProfileSchema))

    def get_background(self, obj):
        return storage.get_url(f"manga/{obj.id}/{obj.background}")

class MangaFormSchema(Schema):
    name = fields.String(required=True)
    name_translations = fields.List(fields.Nested(MangaNameTranslationsSchema), required=False)
    description = fields.String(required=False)
    status = fields.Integer(required=False)
    type = fields.Integer(required=False)
    adult = fields.Integer(required=False)
    genres = fields.Integer(required=False)
    year = fields.Integer(required=False)
    main_poster = fields.Integer(required=False)
    posters = fields.List(fields.String, required=False)
    authors = fields.List(fields.Integer, required=False)
    artists = fields.List(fields.Integer, required=False)
    publishers = fields.List(fields.Integer, required=False)

    @staticmethod
    def _clean_empty_fields(data):
        for key, val in data.items():
            if isinstance(val, str):
                stripped = val.strip()
                if stripped == "":
                    data[key] = None
                else:
                    data[key] = stripped

        return data

    @pre_load
    def preprocess(self, data, **kwargs):
        data = self._clean_empty_fields(data)

        try:
            data["name_translations"] = json.loads(data.get("name_translations") or "null")
        except json.JSONDecodeError as e:
            raise ValidationError({"name_translations": ["Name_translations is invalid"]})

        try:
            data["posters_order"] = json.loads(data.get("posters_order") or "null")
        except json.JSONDecodeError:
            raise ValidationError({"posters_order": ["Posters_order is invalid"]})

        return data
    