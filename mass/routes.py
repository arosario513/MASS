from flask import Blueprint, make_response, redirect, render_template, request, url_for

main: Blueprint = Blueprint("main", __name__)


@main.route("/")
def index() -> str:
    return render_template("index.html", title="Home")


@main.route("/theme", methods=["POST"])
def theme():
    curr: str = request.cookies.get("theme", "light")
    set_theme: str = "dark" if curr == "light" else "light"
    path = request.referrer or url_for("index")
    res = make_response(redirect(path))
    res.set_cookie("theme", set_theme)
    return res
