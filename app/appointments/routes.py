from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user
from flask_login.utils import login_required
from flask_principal import Permission, RoleNeed

from app.appointments.forms import NewAppointment
from app.models import db
from app.models.appointment import Appointment
from app.models.user import User

from . import appointment_blueprint

patient_perm = Permission(RoleNeed("Patient"))
admin_perm = Permission(RoleNeed("Admin"))
dr_perm = Permission(RoleNeed("Doctor"))


@appointment_blueprint.route("/")
@login_required
def view():
    page = request.args.get("page", type=int)
    if admin_perm.can():
        appointments = Appointment.query.order_by(
            Appointment.date, Appointment.time
        ).paginate(page=page, per_page=2)
    elif dr_perm.can():
        appointments = (
            Appointment.query.filter_by(dr_id=current_user.id)
            .order_by(Appointment.date, Appointment.time)
            .paginate(page=page, per_page=2)
        )
    elif patient_perm.can():
        appointments = (
            Appointment.query.filter_by(p_id=current_user.id)
            .order_by(Appointment.date, Appointment.time)
            .paginate(page=page, per_page=2)
        )
    else:
        appointments = []
    return render_template(
        "appointments.html", title="Appointments", appointments=appointments, page=page
    )


@appointment_blueprint.route("/new", methods=["GET", "POST"])
@login_required
@patient_perm.require()
def new():
    form = NewAppointment()
    drs = User.query.join(User.roles).filter_by(name="Doctor").all()
    form.doctor.choices = [(d.id, d.fullname()) for d in drs]
    if form.validate_on_submit():
        appointment = Appointment(
            date=form.date.data,
            time=form.time.data,
            p_id=current_user.id,
            dr_id=form.doctor.data,
            reason=form.reason.data,
        )

        has_conflict = Appointment.query.filter_by(
            date=form.date.data,
            time=form.time.data,
            dr_id=form.doctor.data,
        ).first()

        if has_conflict:
            flash("Doctor is booked at that time", "warning")
        else:
            db.session.add(appointment)
            db.session.commit()
            current_user.notify_appointment(appointment)
            flash("Appointment scheduled successfully", "success")
        return redirect(url_for("appointments.view"))
    return render_template("new_appointment.html", title="New Appointment", form=form)


@appointment_blueprint.route("/delete/<int:id>", methods=["POST"])
@login_required
def cancel(id):
    appt = Appointment.query.get_or_404(id)
    if current_user.id != appt.p_id and not admin_perm.can():
        abort(403)

    db.session.delete(appt)
    db.session.commit()
    flash("Appointment cancelled", "success")
    return redirect(url_for("appointments.view"))
