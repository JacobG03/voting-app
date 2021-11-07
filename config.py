import os
from datetime import timedelta


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
  # General
  SECRET_KEY = os.environ.get('SECRET_KEY') or '$@ul-tra-safe-secret-key$@'
  # Database config
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_IRL') or \
    'sqlite:///' + os.path.join(basedir, 'app.db')
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SESSION_TYPE = 'filesystem'

  # JWT config
  JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", 'local-secret')
  JWT_TOKEN_LOCATION = ['cookies']
  JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=1800)
  JWT_COOKIE_SECURE = False
  JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=15)
  JWT_COOKIE_CSRF_PROTECT = False   # Change to True on Production build 
  JWT_ACCESS_CSRF_HEADER_NAME = "X-CSRF-TOKEN-ACCESS"
  JWT_REFRESH_CSRF_HEADER_NAME = "X-CSRF-TOKEN-REFRESH"