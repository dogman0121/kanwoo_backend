from marshmallow import fields, Schema, validate


class CommentCreateSchema(Schema):
    text = fields.String(validate=[validate.Length(max=1000)])


class CommentSchema(Schema):
    id = fields.Integer()
    text = fields.String()
    creator = fields.Nested("ProfileSchema")
    created_at = fields.DateTime()
    answers_count = fields.Integer()


class CommentPatchVoteSchema(Schema):
    vote = fields.Integer()