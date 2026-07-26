from marshmallow import fields, Schema, validate


class CommentCreateSchema(Schema):
    parent = fields.Integer(allow_none=True)
    manga = fields.Integer(allow_none=True)
    chapter = fields.Integer(allow_none=True)
    text = fields.String(validate=[validate.Length(max=1000)])

"""
id
text
user
answers_count
created_at
up_votes
down_votes
user_vote
"""
class CommentSchema(Schema):
    id = fields.Integer()
    text = fields.String()
    creator = fields.Nested("ProfileSchema")
    created_at = fields.DateTime()
    answers_count = fields.Integer()


class CommentPatchVoteSchema(Schema):
    vote = fields.Integer()