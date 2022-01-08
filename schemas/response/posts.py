from typing_extensions import Required
from marshmallow import Schema, fields, validate


class PostCreateResponseSchema(Schema):
    pk = fields.Integer(required=True)
    title = fields.String(required=True, validate=validate.Length(min=10, max=200))
    post_content = fields.String(required=True)
    date_posted = fields.DateTime(required=True)
