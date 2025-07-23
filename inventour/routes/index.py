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

bp = Blueprint("index", __name__)
@bp.route("/")
def index():
    db = get_db()
    data = db.execute(
        "SELECT c.name as category, s.name as subcategory FROM category c JOIN subcategory s ON c.id = s.category_id ORDER BY c.name, s.name"
      ).fetchall()
    return render_template("management/index.html", data=data)


@bp.route("/create", methods=("POST","GET"))
@login_required
def create():
    if request.method == "POST":
        category = request.form["category"].strip() # .strip() to remove leading/trailing whitespace
        subcategory = request.form["subcategory"].strip() # .strip() to remove leading/trailing whitespace
        db = get_db()
        error = None
        
        if not category:
            error = "Category is required."
        elif not subcategory:
            error = "Subcategory is required."
                       
        if error is None:
            category_row = db.execute("SELECT * FROM category WHERE name = ?", (category,)).fetchone()
            category_id = None

            if category_row is None:
                # Category does not exist, insert it
                try:
                    db.execute("INSERT INTO category (name) VALUES (?)", (category,))
                    db.commit()
                    
                except db.IntegrityError: # Catch specific integrity error for unique constraint
                    error = f"An error occurred while adding the category '{category}'."
                    # This specific error might indicate a race condition or a unique constraint not caught by fetchone
                    # But for simplicity, we assume the fetchone check is usually sufficient.
                except Exception as e:
                    error = f"An unexpected error occurred: {e}"
            else:
                # Category already exists, get its ID
                category_id = category_row["id"]
            
            if error is None and category_id is not None:
                try:
                    db.execute("INSERT INTO subcategory (name, category_id) VALUES (?,?)", (subcategory, category_id))
                    db.commit()
                    return redirect(url_for("index.index"))
                except db.IntegrityError: # Catch specific integrity error for unique constraint on subcategory
                    error = f"Subcategory '{subcategory}' already exists under category '{category}'."
                except Exception as e:
                    error = f"An unexpected error occurred: {e}"
        
        flash(error)

    return render_template("management/create.html")



@bp.route("/add_product", methods=("POST","GET"))
@login_required
def add_product():
    db = get_db()
    data = db.execute(
        "SELECT c.name as category, s.name as subcategory FROM category c JOIN subcategory s ON c.id = s.category_id ORDER BY c.name, s.name"
    ).fetchall()
    return render_template("management/create.html", data=data)