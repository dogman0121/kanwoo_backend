from marshmallow import Schema, fields
from enum import Enum

from .entities import ReadingStartTypeEnum

class DeleteReadingHistoryModeEnum(Enum):
    ALL = "all"
    SELECTED = "selected"

class CreateReadingProgressSchema(Schema):
    chapter_id = fields.Integer()
    page = fields.Integer(allow_none=True)

class GetReadingHistorySchema(Schema):
    id = fields.Integer()
    created_at = fields.DateTime()

class GetReadingHistoryContextSchema(Schema):
    chapter = fields.Nested("GetChapterSchemaMini", allow_none=True)
    manga = fields.Nested("GetMangaSchemaMini", allow_none=True)
    translation = fields.Nested("GetTranslationSchemaMini", allow_none=True)

class DeleteReadingHistorySchema(Schema):
    mode = fields.Enum(DeleteReadingHistoryModeEnum, by_value=True)
    hystory_ids = fields.List(fields.Integer(), allow_none = True)

class UpdateReadingSessionSchema(Schema):
    chapter_id = fields.Integer()
    page = fields.Integer()
    is_finished = fields.Boolean()

class GetReadingBookmarkSchema(Schema):
    id = fields.Integer()
    page = fields.Integer()
    chapter = fields.Nested("GetChapterSchemaMini")

class GetReadingBookmarkContextSchema(Schema):
    chapter = fields.Nested("GetChapterSchemaMini")
    manga = fields.Nested("GetMangaSchemaMini")

class GetChapterProgressSchema(Schema):
    page = fields.Integer()

class GetReadingStartSchema(Schema):
    start_type = fields.Enum(ReadingStartTypeEnum, by_value=True)
    chapter = fields.Nested('GetChapterSchemaMini')