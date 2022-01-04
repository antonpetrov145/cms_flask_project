from marshmallow import Schema, fields, validate


class PostCreateRequestSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=10, max=200))
    post_content = fields.String(required=True)
