#!venv/bin/python

from flask_login import current_user, login_required
from . import admin_blueprint
from app.admin.forms import Edit, NewAccount
from app.models import db
from app.models.role import Role
from app.models.user import User
from argon2 import PasswordHasher
from flask import abort, flash, redirect, render_template, request, url_for
from flask_principal import Permission, RoleNeed

ph: PasswordHasher = PasswordHasher()
admin_perm = Permission(RoleNeed("Admin"))


@admin_blueprint.route("/accounts")
@login_required
@admin_perm.require()
def accounts():
    page = request.args.get("page", type=int)
    users = User.query.paginate(page=page, per_page=3)
    return render_template("accounts.html", title="Accounts", users=users, page=page)


@admin_blueprint.route("/accounts/edit/<int:uid>", methods=["GET", "POST"])
@login_required
@admin_perm.require()
def edit(uid: int):
    user = db.session.get(User, uid)

    if not user:
        abort(404)

    form = Edit(
        og_first_name=user.first_name, og_last_name=user.last_name, og_email=user.email
    )

    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data
        selected_role = form.role.data

        role = db.session.execute(
            db.select(Role).filter_by(name=selected_role)
        ).scalar_one_or_none()

        if role:
            user.roles = [role]
            flash("Updated user", "success")
            db.session.commit()

        else:
            flash("Invalid role", "danger")

        return redirect(url_for("admin.accounts"))

    if request.method == "GET":
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.email.data = user.email

        if user.roles:
            form.role.data = user.roles[0].name

    return render_template("edit.html", title="Edit Account", user=user, form=form)


@admin_blueprint.route("/accounts/new", methods=["GET", "POST"])
@login_required
@admin_perm.require()
def new():
    form = NewAccount()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data
        role = form.role.data

        assert password is not None
        hash = ph.hash(password)

        user = User(
            first_name=first_name, last_name=last_name, email=email, password=hash
        )
        user.add_role(role)

        db.session.add(user)
        db.session.commit()
        user.account_created()
        flash("New account added", "success")
        return redirect(url_for("admin.accounts"))
    return render_template("new_account.html", title="New Account", form=form)


@admin_blueprint.route("/accounts/delete/<int:uid>", methods=["POST"])
@login_required
@admin_perm.require()
def delete_user(uid: int):
    user = User.query.get_or_404(uid)
    if user.ap_as_patient or user.ap_as_doctor:
        flash("This user still has scheduled appointments.", "warning")
        return redirect(url_for("admin.accounts"))

    if uid == current_user.id:
        flash("This user cannot be deleted", "danger")
        return redirect(url_for("admin.accounts"))

    if not user:
        abort(404)

    db.session.delete(user)
    db.session.commit()

    flash("User deleted", "success")
    return redirect(url_for("admin.accounts"))
