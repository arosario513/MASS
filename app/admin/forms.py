from flask_wtf import FlaskForm
from wtforms import (
    EmailField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    ValidationError,
)
from wtforms.validators import DataRequired, EqualTo, Length

from app.models import db
from app.models.role import Role
from app.models.user import User


class Edit(FlaskForm):
    def __init__(
        self, og_first_name=None, og_last_name=None, og_email=None, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.og_first_name = og_first_name
        self.og_last_name = og_last_name
        self.og_email = og_email
        self.role.choices = [
            (r.name, r.name) for r in db.session.execute(db.select(Role)).scalars()
        ]

    first_name = StringField(
        "First Name",
        validators=[DataRequired(), Length(min=3, max=32)],
        render_kw={"placeholder": "First Name"},
    )
    last_name = StringField(
        "Last Name",
        validators=[DataRequired(), Length(min=3, max=32)],
        render_kw={"placeholder": "Last Name"},
    )
    email = EmailField(
        "Email",
        validators=[
            DataRequired(),
            Length(max=32),
        ],
        render_kw={"placeholder": "Email"},
    )
    role = SelectField(
        "Role",
        choices=[],
    )
    submit = SubmitField("Confirm")

    def validate_email(self, email: EmailField):
        if email.data != self.og_email:
            if db.session.execute(db.select(User).filter_by(email=email.data)).first():
                raise ValidationError("User with this email already exists")


class NewAccount(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role.choices = [
            (r.name, r.name) for r in db.session.execute(db.select(Role)).scalars()
        ]

    first_name = StringField(
        "First Name",
        validators=[DataRequired(), Length(min=3, max=32)],
        render_kw={"placeholder": "First Name"},
    )
    last_name = StringField(
        "Last Name",
        validators=[DataRequired(), Length(min=3, max=32)],
        render_kw={"placeholder": "Last Name"},
    )
    email = EmailField(
        "Email",
        validators=[
            DataRequired(),
            Length(max=32),
        ],
        render_kw={"placeholder": "Email"},
    )
    verify_email = EmailField(
        "Email",
        validators=[DataRequired(), EqualTo("email")],
        render_kw={"placeholder": "Verify Email"},
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=8)],
        render_kw={"placeholder": "Password"},
    )
    verify_password = PasswordField(
        "Verify Password",
        validators=[DataRequired(), EqualTo("password")],
        render_kw={"placeholder": "Verify Password"},
    )
    role = SelectField(
        "Role",
        choices=[],
    )
    submit = SubmitField("Create Account")

    def validate_email(self, email: EmailField):
        if db.session.execute(db.select(User).filter_by(email=email.data)).first():
            raise ValidationError("User with this email already exists")
