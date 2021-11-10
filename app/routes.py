from app import app, db
from app.models import User, Poll, Option, Vote
from flask import jsonify, request
from app.schemas import CreateRegisterSchema, CreateLoginSchema, CreatePollSchema, CreateOptionSchema, CreateVoteSchema
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, set_access_cookies, jwt_required, unset_jwt_cookies, current_user


registerSchema = CreateRegisterSchema()
loginSchema = CreateLoginSchema()
pollSchema = CreatePollSchema()
optionSchema = CreateOptionSchema()
voteSchema = CreateVoteSchema()


@app.get('/api')
def api():
  return jsonify({
    'msg': 'It appears that the API should technically maybe work. :)',
    'routes': [
      '/api/login',
      '/api/polls/:id',
      '/api/polls/:id/options',
      '/api/polls/:id/options/:index',
    ]
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
    return jsonify(errors), 422

  # check whether passwords are identical
  elif data['password'] != data['password2']:
    return jsonify({
        'password': ['Passwords must match'],
        'password2': ['Passwords must match']
      }
    ), 422

  # hash password
  hashed_password = generate_password_hash(data['password'], method='sha256')

  # create user
  user = User(
    username=data['username'],
    email=data['email'],
    avatar=data['avatar'],
    password=hashed_password
  )
  db.session.add(user)
  db.session.commit()

  return jsonify({
    'msg': 'User created successfully.'
  }), 200


@app.post('/api/login')
def login():
  response = jsonify({
    'msg': 'Login successfull.'
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
    'msg': 'Logged out successfully.'
  })
  unset_jwt_cookies(response)
  return response, 200


#? Get all polls
@app.get('/api/polls')
def get_polls():
  polls = []
  for poll in Poll.query.order_by(Poll.id.desc()).all():
    polls.append({
      'id': poll.id,
      'votes': len(poll.votes),
      'author_url': f'/users/{poll.user_id}',
      'timestamp': poll.timestamp,
      'topic': poll.topic,
      'options_url': f'/polls/{poll.id}/options',
      'votes_url': f'/polls/{poll.id}/votes'
    })
  return jsonify(polls), 200


#? Get specific poll
@app.get('/api/polls/<id>')
def get_poll(id):
  poll = Poll.query.get(int(id))
  if not poll:
    return jsonify({
      'msg': f'Poll with id: {id} does not exist.'
    }), 500
  
  return jsonify({
    'id': poll.id,
    'votes': len(poll.votes),
    'author_url': f'/users/{poll.user_id}',
    'topic': poll.topic,
    'timestamp': poll.timestamp,
    'options_url': f'/polls/{poll.id}/options',
    'votes_url': f'/polls/{poll.id}/votes'
  }), 200


#? Create Poll
@app.post('/api/polls')
@jwt_required()
def create_poll():
  # receive data
  data = request.get_json(silent=True)
  # validate data
  errors = pollSchema.validate(data)
  if errors:
    return jsonify({
      'errors': errors
    }), 422
  
  # create poll
  poll = Poll(user_id=current_user.id, topic=data['topic'])
  db.session.add(poll)
  db.session.commit()

  # create given options
  for body in data['options']:
    option = Option(poll_id=poll.id, body=body)
    db.session.add(option)
  db.session.commit()
  
  return jsonify({
    'msg': 'Poll created.'
  }), 200


#? Delete Poll
@app.delete('/api/polls/<id>')
@jwt_required()
def delete_poll(id):
  poll = Poll.query.get(int(id))
  if not poll:
    return jsonify({
      'msg': 'Poll with id: {id} does not exist.'
    }), 500
  
  if poll.user_id != current_user.id:
    return jsonify({
      'msg': 'Action denied.'
    }), 500

  # deletes poll
  poll.desctruction()
  db.session.commit()

  return jsonify({
    'msg': 'Poll deleted successfully.'
  }), 200


#? Get all options of specified poll
@app.get('/api/polls/<poll_id>/options')
def get_options(poll_id):
  response = []
  poll = Poll.query.get(int(poll_id))
  if not poll:
    return jsonify({
      'msg': f'Poll with id: {poll_id} does not exist'
    }), 500
  
  for index, option in enumerate(poll.options):
    response.append({
      'index': index,
      'body': option.body,
      'votes_url': f'/polls/{poll_id}/options/{index}/votes'
    })
  
  return jsonify(response), 200


#? Get specific option of a specific poll
@app.get('/api/polls/<poll_id>/options/<index>')
def get_option(poll_id, index):
  poll = Poll.query.get(int(poll_id))
  # throw error if poll doesnt exist
  if not poll:
    return jsonify({
      'msg': 'Poll with id: {id} does not exist.'
    }), 500
  
  try:
    option = poll.options[int(index)]
  except IndexError:
    return jsonify({
      'msg': f'Poll with index: {index} does not exist'
    }), 500

  # if all OK
  return jsonify({
    'index': index,
    'body': option.body,
    'votes_url': f'/polls/{poll_id}/options/{index}/votes',
    'poll_url': f'/polls/{poll_id}'
  }), 200


"""
#! Unnecessary for this project, polls will be created once and without ability to edit
#! Reason for this is that changing context of a poll sucks + it will make implementing socketio harded
#? Create option for a specific pool
@app.post('/api/polls/<poll_id>/options')
@jwt_required()
def create_option(poll_id):
  poll = Poll.query.get(int(poll_id))
  # throw error if poll doesnt exist
  if not poll:
    return jsonify({
      'msg': 'Poll with id: {id} does not exist.'
    }), 500

  # receive data
  data = request.get_json(silent=True)
  # validate data
  errors = optionSchema.validate(data)
  if errors:
    return jsonify({
      'errors': errors,
    }), 422

  # check if its unique in its own poll
  if any(option.body for option in poll.options if option.body == data['body']):
    return jsonify({
      'errors': {
        'body': ['Each option must be unique.']
      }
    }), 422

  option = Option(poll_id=poll.id, body=data['body'])
  db.session.add(option)
  db.session.commit()

  return jsonify({
    'msg': 'Option added.'
  }), 200
"""

@app.get('/api/user')
@jwt_required()
def user():
  return jsonify({
    'id': current_user.id,
    'username': current_user.username,
    'avatar': current_user.avatar
  }), 200


@app.get('/api/users')
def get_users():
  # return users data
  users = []
  for user in User.query.all():
    users.append({
      'id': user.id,
      'username': user.username,
      'avatar': user.avatar
    })
  return jsonify(users), 200


@app.get('/api/users/<id>')
def get_user(id):
  # check if user exists
  user = User.query.get(int(id))
  if not user:
    return jsonify({
      'msg': f'User with id: {id} does not exist'
    }), 500
  
  # return user data
  return jsonify({
    'id': user.id,
    'username': user.username,
    'avatar': user.avatar
  }), 200


#? Create Vote
@app.post('/api/polls/<poll_id>/options/<index>/votes')
@jwt_required()
def vote(poll_id, index):
  poll = Poll.query.get(int(poll_id))
  # throw error if poll doesnt exist
  if not poll:
    return jsonify({
      'msg': 'Poll with id: {id} does not exist.'
    }), 500
  
  try:
    option = poll.options[int(index)]
  except IndexError:
  # throw error if option doesnt exist
    return jsonify({
      'msg': f'Poll with index: {index} does not exist'
    }), 500

  # receive data
  data = request.get_json(silent=True)
  errors = voteSchema.validate(data)
  if errors:
    return jsonify(errors), 422
  
  # do nothing if user already voted
  if poll.did_vote(current_user.id):
    return jsonify({
      'msg': 'You can only vote once.'
    }), 200
  
  vote = Vote(
    anonymous=data['anonymous'], 
    user_id=current_user.id, 
    poll_id=poll.id,
    option_id=option.id
    )
  
  db.session.add(vote)
  db.session.commit()

  return jsonify({
    'msg': 'Voted successfully.'
  }), 200


#? Get Polls Votes
@app.get('/api/polls/<poll_id>/votes')
@jwt_required()
def get_poll_votes(poll_id):
  poll = Poll.query.get(int(poll_id))
  # throw error if poll doesnt exist
  if not poll:
    return jsonify({
      'msg': 'Poll with id: {id} does not exist.'
    }), 500

  # prevent user that didnt vote from seeing the results
  if not poll.did_vote(current_user.id):
    return jsonify({}), 202
  
  votes = []
  for vote in poll.votes:
    user = User.query.get(vote.user_id)
    votes.append({
      'username': user.username if vote.anonymous == False else 'Human',
      'avatar': user.avatar if vote.anonymous == False else 'https://avatarfiles.alphacoders.com/101/thumb-1920-101741.jpg'
    })
  
  return jsonify(votes), 200


#? Get Option's Votes
@app.get('/api/polls/<poll_id>/options/<index>/votes')
@jwt_required()
def get_option_votes(poll_id, index):
  poll = Poll.query.get(int(poll_id))
  # throw error if poll doesnt exist
  if not poll:
    return jsonify({
      'msg': 'Poll with id: {id} does not exist.'
    }), 500
  
  try:
    option = poll.options[int(index)]
  except IndexError:
  # throw error if option doesnt exist
    return jsonify({
      'msg': f'Poll with index: {index} does not exist'
    }), 500

  # prevent user that didnt vote from seeing the results
  if not poll.did_vote(current_user.id):
    return jsonify({}), 202

  votes = []
  for vote in option.votes:
    user = User.query.get(vote.user_id)
    votes.append({
      'username': user.username if vote.anonymous == False else 'Human',
      'avatar': user.avatar if vote.anonymous == False else 'https://avatarfiles.alphacoders.com/101/thumb-1920-101741.jpg'
    })
  
  return jsonify({
    'voted': option.did_vote(current_user.id),
    'votes': votes
  }), 200