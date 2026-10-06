from marshmallow import fields, Schema, validate


class CreateCommentSchema(Schema):
    text = fields.String(validate=[validate.Length(max=1000)])
    manga_id = fields.Integer()
    chapter_id = fields.Integer()


class GetCommentSchema(Schema):
    id = fields.Integer()
    text = fields.String()
    creator = fields.Nested("ProfileSchema")
    created_at = fields.DateTime()
    answers_count = fields.Integer()

class GetCommentViewerContext(Schema):
    vote = fields.Integer()

class GetCommentContext(Schema):
    viewer = fields.Nested(GetCommentViewerContext)

class GetDiscussionCommentSchema(GetCommentSchema):
    reply_to = fields.Nested("GetProfileSchema")

class GetDiscussionCommentContextSchema(GetCommentContext):
    pass

class GetSubthreadSchema(Schema):
    root_comment = fields.Nested(GetCommentSchema)
    discussion = fields.List(fields.Nested(GetDiscussionCommentSchema))
    discussion_cursor = fields.Raw()

class GetSubthreadContextSchema(Schema):
    head_comment = fields.Nested(GetCommentContext)
    discussion = fields.List(fields.Nested(GetCommentContext))

class VoteSchema(Schema):
    vote = fields.Integer()