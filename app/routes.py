from app import app, db
from app.models import User, Poll
from flask import json, jsonify, request
from app.schemas import CreateRegisterSchema, CreateLoginSchema
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, set_access_cookies, jwt_required, unset_jwt_cookies, current_user


registerSchema = CreateRegisterSchema()
loginSchema = CreateLoginSchema()


@app.get('/api')
@jwt_required()
def api():
  return jsonify({
    'message': 'It appears that the API should technically maybe work. :)'
  }), 200


@app.get('/api/refresh')
@jwt_required()
def refresh():
  response = jsonify()
  access_token = create_access_token(identity=current_user)
  set_access_cookies(response, access_token)
  return response, 200


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


@app.get('/api/logout')
def logout():
  response = jsonify({
    'message': 'Logged out successfully.'
  })
  unset_jwt_cookies(response)
  return response, 200


#? Get polls
@app.get('/api/polls')
@jwt_required()
def get_polls():
  polls = []
  for poll in Poll.query.all():
    polls.append({
      'id': poll.id,
      'topic': poll.topic,
      'options': f'/polls/{poll.id}/options',
      'votes': f'/polls/{poll.id}/votes'
    })
  return jsonify({
    'polls': polls
  }), 200


#? Create Poll
@app.post('/api/polls')
@jwt_required()
def create_poll():
  #! Code
  return jsonify({
    'message': 'Poll created.'
  }), 200