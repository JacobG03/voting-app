from app import app, db
from app.models import User
from flask import jsonify, request
from app.schemas import CreateRegisterSchema
from werkzeug.security import generate_password_hash, check_password_hash


registerSchema = CreateRegisterSchema()


@app.get('/api')
def api():
  return jsonify({
    'message': 'It appears that the API should technically maybe work. :)'
  }), 200


@app.post('/api/register')
def register():
  # receives data
  data = request.get_json(silent=True)
  # validate data
  errors = registerSchema.validate(data)
  if errors:
    return jsonify({
      'errors': errors
    }), 422

  # checks whether passwords are identical
  elif data['password'] != data['password2']:
    return jsonify({
      'errors': {
        'password': ['Passwords must match'],
        'password2': ['Passwords must match']
      }
    }), 422

  # hash password
  hashed_password = generate_password_hash(data['password'], method='sha256')

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


