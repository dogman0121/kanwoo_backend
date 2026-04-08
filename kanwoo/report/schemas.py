from marshmallow import Schema, fields


class ReportCreateSchema(Schema):
    type=fields.Integer()
    comment=fields.String()