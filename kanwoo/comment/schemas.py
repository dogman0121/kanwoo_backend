from marshmallow import fields, Schema, validate, pre_dump


class CreateCommentSchema(Schema):
    text = fields.String(validate=[validate.Length(max=1000)])
    manga_id = fields.String(allow_none=True)
    chapter_id = fields.Integer(allow_none=True)


class GetCommentSchema(Schema):
    id = fields.Integer()
    text = fields.String()
    creator = fields.Nested("GetProfileSchema")
    created_at = fields.DateTime()
    replies_count = fields.Integer()
    up_votes = fields.Integer()
    down_votes = fields.Integer()

class GetCommentViewerContextSchema(Schema):
    vote = fields.Integer()

class GetCommentContextSchema(Schema):
    viewer = fields.Nested(GetCommentViewerContextSchema)

class GetDiscussionCommentSchema(GetCommentSchema):
    reply_to = fields.Nested("GetProfileSchema")

class GetDiscussionCommentContextSchema(GetCommentContextSchema):
    pass

class GetCommentCursor(Schema):
    cursor = fields.Dict(keys=fields.String(), values=fields.Integer())
    has_more = fields.Boolean()


class GetSubthreadSchema(Schema):
    root_comment = fields.Nested(GetCommentSchema)
    discussion = fields.List(fields.Nested(GetDiscussionCommentSchema))
    discussion_pagination = fields.Nested(GetCommentCursor)

class GetSubthreadContextSchema(Schema):
    root_comment = fields.Nested(GetCommentContextSchema)
    discussion = fields.List(fields.Nested(GetCommentContextSchema))

class VoteSchema(Schema):
    vote = fields.Integer()