from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from flask import current_app, flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user
from flask_principal import AnonymousIdentity, Identity, identity_changed

from mass.auth.forms import ForgotPassword, Login, Register, Reset
from mass.models import db
from mass.models.user import User

from . import auth_blueprint

ph = PasswordHasher()

DUMMY_HASH = "$argon2id$v=19$m=65536,t=3,p=4$cn6382O+GKdFP5HGFUqwCA$MazNjdUS2EOk96rL1tHseuf+GGS6mwOclCWozUgi3Aw"


@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = Register()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data

        assert password is not None
        hash = ph.hash(password)
        user = User(
            first_name=first_name, last_name=last_name, email=email, password=hash
        )
        user.add_role("Patient")

        db.session.add(user)
        db.session.commit()
        login_user(user)
        identity_changed.send(
            current_app._get_current_object(), identity=Identity(user.id)
        )
        user.account_created()
        flash(f"Welcome, {user.fullname()}", "success")
        return redirect(url_for("appointments.view"))
    return render_template("register.html", title="Register", form=form)


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = Login()
    if current_user.is_authenticated:
        return redirect(url_for("appointments.view"))

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()

        assert password is not None

        # This is to avoid timing attacks. I know, it's overkill.
        user_hash = user.password if user else DUMMY_HASH

        try:
            is_valid_password = ph.verify(user_hash, password)
        except VerifyMismatchError:
            is_valid_password = False

        if is_valid_password and user:
            login_user(user)
            flash("Logged in", "success")

            identity_changed.send(
                current_app._get_current_object(), identity=Identity(user.id)
            )

            return redirect(url_for("appointments.view"))

        elif user:
            flash("Wrong password", "danger")
        else:
            flash("Invalid login", "danger")

    return render_template("login.html", title="Login", form=form)


@auth_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out", "warning")
    identity_changed.send(auth_blueprint, identity=AnonymousIdentity)
    return redirect(url_for("auth.login"))


@auth_blueprint.route("/forgot-password", methods=["GET", "POST"])
def forgot():
    form = ForgotPassword()
    if form.validate_on_submit():
        email = form.email.data
        user: User | None = User.query.filter_by(email=email).first()
        if user:
            user.request_password_reset()
            flash("Request for password reset sent", "success")
        return redirect(url_for("auth.login"))
    return render_template("forgot.html", title="Forgot Password", form=form)


@auth_blueprint.route("/reset/<token>", methods=["GET", "POST"])
def reset(token: str):
    user = User.verify_reset_token(token)
    if not user:
        flash("Invalid token", "danger")
        return redirect(url_for("auth.login"))
    form = Reset()
    if form.validate_on_submit():
        password = form.password.data
        assert password is not None
        hash = ph.hash(password)
        user.password = hash
        db.session.commit()
        flash("Password changed", "success")
        return redirect(url_for("auth.login"))
    return render_template("reset.html", title="Reset Password", form=form)
