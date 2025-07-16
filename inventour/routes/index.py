from flask import (
  Blueprint,
  render_template,
  url_for,
  redirect,
  request,
  flash,
  g
  )

from werkzeug.exceptions import abort

from inventour.routes.auth.auth import login_required
from inventour.db import get_db

bp = Blueprint("inventory", __name__)
@bp.route("/")
def index():
    db = get_db()
    subcategories = db.execute(
        "SELECT * FROM subcategory"
      ).fetchall()
    return render_template("management/index.html", subcategories=subcategories)
