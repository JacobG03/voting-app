from app import db
from datetime import datetime


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), unique=True, nullable=False)
  email = db.Column(db.String(128), unique=True, nullable=False)    # In this case doesn't have to be an actual email
  password = db.Column(db.String(256), nullable=False)
  avatar = db.Column(db.String(512), default='https://avatarfiles.alphacoders.com/101/thumb-1920-101741.jpg', nullable=True)
  votes = db.relationship('Vote', backref=db.backref('user', lazy=True))

  def __repr__(self):
    return f'{self.username}'


class Poll(db.Model):
  """
  Poll(user_id, topic)
  """
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  topic = db.Column(db.String(256), nullable=False)
  options = db.relationship('Option', backref=db.backref('poll', lazy=True))
  votes = db.relationship('Vote', backref=db.backref('poll', lazy=True))
  timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)


  def desctruction(self):
    # delete all option votes
    self.delete_votes()
    # delete all options
    self.delete_options()
    # delete self
    db.session.delete(self)
    return True

  def delete_votes(self):
    for vote in self.votes:
      db.session.delete(vote)
    return True

  def delete_options(self):
    for option in self.options:
      db.session.delete(option)
    return True


  def did_vote(self, id):
    """
    did_vote(user_id)
    Returns True if user voted in this poll already
    """
    return any([user.id for user in self.votes if user.id == id])

  def __repr__(self):
    return f'{self.topic}'


class Option(db.Model):
  """
  Option(poll_id, body)
  """
  id = db.Column(db.Integer, primary_key=True)
  poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)
  body = db.Column(db.String(128), nullable=False)
  votes = db.relationship('Vote', backref=db.backref('option', lazy=True))

  def __repr__(self):
    return f'{self.body}'


class Vote(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  anonymous = db.Column(db.Boolean, default=True, nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)
  option_id = db.Column(db.Integer, db.ForeignKey('option.id'), nullable=False)

  def __repr__(self):
    return f'{Option.query.get(self.id).body}'
