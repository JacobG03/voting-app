from app import app, db
from app.models import User, Poll, Option, Vote


@app.shell_context_processor
def make_shell_context():
  return {
    'db': db,
    'User': User,
    'Poll': Poll,
    'Option': Option,
    'Vote': Vote
  }


if __name__ == "__main__":
  app.run()