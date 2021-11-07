from app import db


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), unique=True, nullable=False)
  email = db.Column(db.String(128), unique=True, nullable=False)    # In this case doesn't have to be an actual email
  password = db.Column(db.String(256), nullable=False)

  def __repr__(self):
    return f'{self.username}'


