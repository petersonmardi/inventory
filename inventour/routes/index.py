from flask import (
  Blueprint,
  render_template,
  url_for,
  session,
  redirect,
  request,
  flash,
  g
  )

bp = Blueprint('index', __name__)
@bp.route('/')
def index():
    return "Hi! Start writing your app codes."
