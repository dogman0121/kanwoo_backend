from marshmallow import Schema, fields
from dataclasses import dataclass
from enum import Enum
from typing import Optional
from datetime import datetime


class FrontentMetadataResouceTypeEnum(Enum):
    WEBSITE = "website"
    BOOK = "book"
    ARTICLE = "acticle"

class FrontendMetadataSchema(Schema):
    title = fields.String()
    description = fields.String()
    canonical = fields.String()
    image = fields.String(allow_none=True)
    type = fields.Enum(FrontentMetadataResouceTypeEnum, by_value=True)
    indexable = fields.Boolean()
    published_at = fields.DateTime(allow_none=True)
    modified_at = fields.DateTime(allow_none=True)

@dataclass
class FrontendMetadataDTO:
    title: str
    description: str
    canonical: str
    image: Optional[str]
    type: FrontentMetadataResouceTypeEnum
    indexable: bool
    published_at: Optional[datetime]
    modified_at: Optional[datetime]

class FrontendMetadataServiceMixin:

    def get() -> FrontendMetadataDTO:
        pass