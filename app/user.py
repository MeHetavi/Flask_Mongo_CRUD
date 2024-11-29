from marshmallow import Schema, fields, validate, ValidationError
import re

class UserSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    email = fields.Email(required=True, validate=validate.Email())
    password = fields.Str(
        required=True, 
        validate=validate.Regexp(
            r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', 
            error='Password must be at least 8 characters long and include letters, numbers, and special characters'
        ),
        load_only=True
    )
    
    def validate_email(self, value):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValidationError('Invalid email format')