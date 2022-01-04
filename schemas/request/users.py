from marshmallow import Schema, fields


class BaseUserSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class RequestRegisterUserSchema(BaseUserSchema):
    username = fields.String(min_length=5, max_length=50, required=True)


class RequestRegisterClientUserSchema(BaseUserSchema):
    username = fields.String(min_length=5, max_length=50, required=True)
    iban = fields.String(min_length=22, max_legth=22, required=True)


class RequestLoginAuthorUserSchema(BaseUserSchema):
    pass


class RequestLoginEditorUserSchema(BaseUserSchema):
    pass


class RequestLoginClientUserSchema(BaseUserSchema):
    pass


class RequestLoginAdminUserSchema(BaseUserSchema):
    pass
