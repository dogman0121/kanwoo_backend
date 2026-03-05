from werkzeug.datastructures import FileStorage
from marshmallow import Schema, fields, ValidationError
import json

from kanwoo.entity import convert_to_file

class File(fields.Raw):

    def __init__(self, *args, max_file_size=None, allowed_file_types=None, allowed_file_ext=None, **kwargs):
        self.max_file_size = max_file_size
        self.allowed_file_types = allowed_file_types
        self.allowed_file_ext = allowed_file_ext

        super().__init__(*args, **kwargs)
    
    def _serialize(self, value, attr, obj, **kwargs):
        return None
    
    def _deserialize(self, value, attr, data, **kwargs):

        if not isinstance(value, FileStorage):
            raise ValidationError('Invalid file object', attr)
        
        if self.max_file_size and value.content_length > self.max_file_size:
            raise ValidationError(
                f'File too large: {value.content_length // 1024 // 1024}MB. '
                f'Max: {self.max_file_size // 1024 // 1024}MB', 
                attr
            )
        
        file_ext = value.filename[value.filename.rfind("."):]
        
        if self.allowed_file_ext and file_ext not in self.allowed_file_ext:
            raise ValidationError(
                'Invalid file type.', 
                attr
            )
        
        if self.allowed_file_types and value.content_type not in self.allowed_file_types:
            raise ValidationError('Invalid image format', attr)

        return convert_to_file(value)

class Json(fields.String):
    
    def _serialize(self, value, attr, obj, **kwargs):
        return json.dumps(value)
    
    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return json.loads(value)
        except json.JSONDecodeError as e:
            raise ValidationError("Invalid json", attr)

class PrivacySchema(Schema):
    id = fields.Integer()
    name = fields.String()


class LanguageSchema(Schema):
    id = fields.Integer()
    name = fields.String()