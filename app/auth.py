from app import app, jwt
from app.models import User
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import get_jwt, current_user, create_access_token, set_access_cookies


# Allows creating an access token by passing in a user object
@jwt.user_identity_loader
def user_identity_lookup(user):
  return user.id

# loads a user from your database whenever a protected route is accessed
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
  identity = jwt_data["sub"]
  return User.query.filter_by(id=identity).one_or_none()

@app.after_request
def refresh_expiring_jwts(response):
  try:
    exp_timestamp = get_jwt()["exp"]
    now = datetime.now(timezone.utc)
    target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
    if target_timestamp > exp_timestamp:
      access_token = create_access_token(identity=current_user)
      set_access_cookies(response, access_token)
    return response
  except (RuntimeError, KeyError):
    # Case where there is not a valid JWT. Just return the original respone
    return response