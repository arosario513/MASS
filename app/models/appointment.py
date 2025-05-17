from sqlalchemy.orm import relationship
from . import db


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    reason = db.Column(db.String(64), nullable=True)

    p_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    dr_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    patient = relationship(
        "User",
        foreign_keys=[p_id],
        backref="ap_as_patient"
    )
    doctor = relationship(
        "User",
        foreign_keys=[dr_id],
        backref="ap_as_doctor"
    )

    def __init__(self, date, time, p_id, dr_id, reason):
        self.date = date
        self.time = time
        self.p_id = p_id
        self.dr_id = dr_id
        self.reason = reason

    def __repr__(self):
        return f"Appointment({self.date}, {self.time.strftime("%-I:%M%p")}, {self.p_id}, {self.dr_id})"
