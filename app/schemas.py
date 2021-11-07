from marshmallow import Schema, fields, validates, ValidationError
from marshmallow.validate import Length
import re
from app.models import User
from sqlalchemy import func


class CreateRegisterSchema(Schema):
  username = fields.Str(required=True, validate=Length(3, 64))
  email = fields.Str(required=True,  validate=Length(1, 128))
  password = fields.Str(required=True, validate=Length(4, 128))
  password2 = fields.Str(required=True, validate=[Length(4, 128)])


  @validates('username')
  def validateUsername(self, value):
    username_regex = re.compile(r'^(?![-._])(?!.*[_.-]{2})[\w.-]{3,64}(?<![-._])$')
    if username_regex.match(value) == None:
      raise ValidationError('Username contains invalid characters')
    # Case insensitive query filter
    elif User.query.filter(func.lower(User.username) == func.lower(value)).first():
      raise ValidationError('Username is taken. Try a different one')


  @validates('email')
  def validateEmail(self, email):
    # checks if email is used by another user
    if User.query.filter(func.lower(User.email) == func.lower(email)).first():
      raise ValidationError('Email is taken. Try a different one')


class CreateLoginSchema(Schema):
  email = fields.Str(required=True)
  password = fields.Str(required=True)


class CreatePollSchema(Schema):
  topic = fields.Str(required=True, validate=Length(1, 256))
  options = fields.List(fields.Str(required=True, validate=Length(1, 128)))


class CreateOptionSchema(Schema):
  body = fields.Str(required=True, validate=Length(1, 128))


class CreateVoteSchema(Schema):
  anonymous = fields.Bool(required=True)