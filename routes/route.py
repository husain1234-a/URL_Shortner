from database.db import Database
from utils.validators import is_valid_url
from utils.generators import generate_short_code
from flask import Blueprint, render_template, request, redirect, url_for, flash

main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        original_url = request.form.get("url", "").strip()

        if not original_url:
            flash("URL cannot be empty", "error")
            return redirect(url_for("main.index"))

        if len(original_url) <= 1:
            flash("URL must be longer than 1 character", "error")
            return redirect(url_for("main.index"))

        is_valid, error_message = is_valid_url(original_url)
        if not is_valid:
            flash(error_message, "error")
            return redirect(url_for("main.index"))

        db_model = Database()
        existing_short_url = db_model.get_short_url(original_url)

        if existing_short_url is None:
            short_code = generate_short_code()
        else:
            short_code = existing_short_url

        try:
            db_model.create_short_url(original_url, short_code)
        except ValueError:
            flash("This URL has already been shortened", "error")
            return redirect(url_for("main.index"))

        short_url = url_for(
            "main.redirect_to_url", short_code=short_code, _external=True
        )
        flash(f"Your shortened URL: {short_url}", "success")
        return redirect(url_for("main.index"))

    return render_template("index.html")


@main.route("/<short_code>")
def redirect_to_url(short_code):
    db_model = Database()
    original_url = db_model.get_original_url(short_code)

    if original_url:
        return redirect(original_url)

    flash("Invalid or expired URL")
    return redirect(url_for("main.index"))


@main.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-store, max-age=0"
    return response
