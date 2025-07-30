from json import JSONDecodeError

from marshmallow import fields, Schema, pre_load, ValidationError
import json

from app.api.schemas.manga.manga_name_translations_schema import MangaNameTranslationsSchema


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
    new_posters = fields.List(fields.Raw, required=False)
    posters_order = fields.List(fields.String, required=False)
    background = fields.Raw(required=False)
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
        except JSONDecodeError:
            raise ValidationError({"name_translations": ["Name_translations is invalid"]})

        try:
            data["posters_order"] = json.loads(data.get("posters_order") or "null")
        except JSONDecodeError:
            raise ValidationError({"posters_order": ["Posters_order is invalid"]})

        return data