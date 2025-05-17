from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, StringField, SubmitField, TimeField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import TextArea


class NewAppointment(FlaskForm):
    date = DateField("Date", validators=[DataRequired()])
    time = TimeField("Time", validators=[DataRequired()])
    doctor = SelectField("Doctor", coerce=int, validators=[DataRequired()])
    reason = StringField(
        "Reason",
        widget=TextArea(),
        validators=[
            Length(max=64)
        ],
        render_kw={
            "placeholder": "Reason",
            "style": "resize: none; height: 100px;",
        }
    )
    submit = SubmitField("Book Appointment")
