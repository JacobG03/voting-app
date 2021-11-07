from flask_jwt_extended.view_decorators import jwt_required
from app import app, db
from app.models import User
from flask import jsonify, request
from app.schemas import CreateRegisterSchema, CreateLoginSchema
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, set_access_cookies


registerSchema = CreateRegisterSchema()
loginSchema = CreateLoginSchema()

@app.get('/api')
def api():
  return jsonify({
    'message': 'It appears that the API should technically maybe work. :)'
  }), 200


@app.post('/api/register')
def register():
  # receive data
  data = request.get_json(silent=True)
  # validate data
  errors = registerSchema.validate(data)
  if errors:
    return jsonify({
      'errors': errors
    }), 422

  # check whether passwords are identical
  elif data['password'] != data['password2']:
    return jsonify({
      'errors': {
        'password': ['Passwords must match'],
        'password2': ['Passwords must match']
      }
    }), 422

  # hash password
  hashed_password = generate_password_hash(data['password'], method='sha256')

  # create user
  user = User(
    username=data['username'],
    email=data['email'],
    password=hashed_password
  )
  db.session.add(user)
  db.session.commit()

  return jsonify({
    'message': 'User created successfully.'
  }), 200


@app.post('/api/login')
def login():
  response = jsonify({
    'message': 'Login successfull.'
  })
  # receive data
  data = request.get_json(silent=True)
  # validate data
  errors = loginSchema.validate(data)
  if errors:
    return jsonify({
      'errors': errors
    }), 422

  # check if user exists
  user = User.query.filter_by(email=data['email']).first()
  if user and check_password_hash(user.password, data['password']):
    # crate token
    access_token = create_access_token(identity=user)
    # set token cookie in browser
    set_access_cookies(response, access_token)

    return response

  
  return jsonify({
      'errors': {
        'email': ['Invalid fields'],
        'password': ['Invalid fields']
      }
    }), 422