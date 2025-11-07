from werkzeug.datastructures import FileStorage
from marshmallow import Schema, fields, pre_load, ValidationError, validate

import json

from app import storage
from app.profile.schemas import ProfileSchema
from app.entity import to_file
from app.entity import FileAction

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

class MangaTranslationSchema(Schema):
    id = fields.Integer()
    created_at = fields.DateTime()
    creator = fields.Nested(ProfileSchema)

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
    views = fields.Integer()
    poster = fields.Nested(MangaPosterSchema)
    background = fields.Method("get_background")
    promo_name = fields.Method("get_promo_name")
    promo_logo = fields.Method("get_promo_logo")
    promo_background = fields.Method("get_promo_background")
    authors = fields.List(fields.Nested(ProfileSchema))
    artists = fields.List(fields.Nested(ProfileSchema))
    publishers = fields.List(fields.Nested(ProfileSchema))
    creator = fields.Nested(ProfileSchema)
    created_at = fields.DateTime()

    def get_background(self, obj):
        if obj.background:
            return storage.get_url(f"manga/{obj.background.uuid}{obj.background.ext}")
        return None
    
    def get_promo_name(self, obj):
        if obj.promo_name:
            return storage.get_url(f"manga/{obj.promo_name.uuid}{obj.promo_name.ext}")
        return None

    def get_promo_logo(self, obj):
        if obj.promo_logo:
            return storage.get_url(f"manga/{obj.promo_logo.uuid}{obj.promo_logo.ext}")
        return None

    def get_promo_background(self, obj):
        if obj.promo_background:
            return storage.get_url(f"manga/{obj.promo_background.uuid}{obj.promo_background.ext}")
        return None

class MangaCreateSchema(Schema):
    name = fields.String()

class MangaUpdateSchema(Schema):
    slug = fields.String()
    name = fields.String()
    name_translations = fields.List(fields.Nested(MangaNameTranslationsSchema), allow_none=True)
    description = fields.String(allow_none=True)
    status = fields.Integer()
    type = fields.Integer()
    adult = fields.Integer()
    genres = fields.List(fields.Integer())
    year = fields.Integer()
    authors = fields.List(fields.Integer, allow_none=True)
    artists = fields.List(fields.Integer, allow_none=True)
    publishers = fields.List(fields.Integer, allow_none=True)
    background = fields.Raw(allow_none=True)
    poster = fields.Raw(allow_none=True)
    background_action = fields.Enum(FileAction, by_value=True)
    poster_action = fields.Enum(FileAction, by_value=True)
    promo_name = fields.Raw(allow_none=True)
    promo_logo = fields.Raw(allow_none=True)
    promo_background = fields.Raw(allow_none=True)
    promo_name_action = fields.Enum(FileAction, by_value=True)
    promo_logo_action = fields.Enum(FileAction, by_value=True)
    promo_background_action = fields.Enum(FileAction, by_value=True)

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.allowed_image_types = ['image/jpeg', 'image/png', 'image/webp']
        self.allowed_extensions = ['.jpeg', '.jpg', '.png', '.webp']
        self.max_file_size = 10 * 1024 * 1024

    def _process_image_file(self, file, field_name):
        if not isinstance(file, FileStorage):
            raise ValidationError('Invalid file object', field_name)
        if file.content_length > self.max_file_size:
            raise ValidationError(
                f'File too large: {file.content_length // 1024 // 1024}MB. '
                f'Max: {self.max_file_size // 1024 // 1024}MB', 
                field_name
            )
        
        file_ext = file.filename[file.filename.rfind("."):]
        
        if file_ext not in self.allowed_extensions:
            raise ValidationError(
                'Invalid file type.', 
                field_name
            )
        
        if file.content_type not in self.allowed_image_types:
            raise ValidationError('Invalid image format', field_name)

        return to_file(file)

    @pre_load
    def preprocess(self, data, **kwargs):
        data = self._clean_empty_fields(data)

        if "name_translations" in data and data["name_translations"] is not None:
            try:
                data["name_translations"] = json.loads(data.get("name_translations"))
            except json.JSONDecodeError as e:
                raise ValidationError({"name_translations": ["Name translations is invalid"]})
            
        if "background" in data and data["background"] is not None:
            data["background"] = self._process_image_file(data["background"], "background")
        
        if "poster" in data and data["poster"] is not None:
            data["poster"] = self._process_image_file(data["poster"], "poster")
        
        if "promo_name" in data and data["promo_name"] is not None:
            data["promo_name"] = self._process_image_file(data["promo_name"], "promo_name")
        
        if "promo_logo" in data and data["promo_logo"] is not None:
            data["promo_logo"] = self._process_image_file(data["promo_logo"], "promo_logo")

        if "promo_background" in data and data["promo_background"] is not None:
            data["promo_background"] = self._process_image_file(data["promo_background"], "backgrpromo_backgroundound")

        return data
    

        
    