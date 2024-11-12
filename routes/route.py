from database.db import Database
from utils.validators import is_valid_url
from utils.generators import generate_short_code
from flask import Blueprint, render_template, request, redirect, url_for, flash

main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        original_url = request.form["url"]
        if not is_valid_url(original_url):
            flash("Invalid URL format")
            return render_template("index.html")

        url_model = Database()
        x = str(original_url)
        if url_model.get_short_url(x) is None:
            short_code = generate_short_code()
        else:
            short_code = url_model.get_short_url(original_url)

        url_model.create_short_url(original_url, short_code)

        short_url = url_for(
            "main.redirect_to_url", short_code=short_code, _external=True
        )
        return render_template("index.html", short_url=short_url)

    return render_template("index.html")


@main.route("/<short_code>")
def redirect_to_url(short_code):
    url_model = Database()
    original_url = url_model.get_original_url(short_code)

    if original_url:
        return redirect(original_url)

    flash("Invalid or expired URL")
    return redirect(url_for("main.index"))
