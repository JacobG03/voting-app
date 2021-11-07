from app import app
from flask import jsonify


@app.get('/api')
def api():
  return jsonify({
    'message': 'It appears that the API should technically maybe work. :)'
  }), 200