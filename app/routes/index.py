from flask import (
  Blueprint,
  render_template,
  url_for,
  )

bp = Blueprint('index', __name__)
@bp.route('/')
def index():
    return "Hi! Start writing your app codes."
