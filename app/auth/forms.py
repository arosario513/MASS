from flask_wtf import FlaskForm
from app.models import db
from app.models.user import User
from wtforms import (
    EmailField,
    PasswordField,
    StringField,
    SubmitField,
    ValidationError
)
from wtforms.validators import DataRequired, EqualTo, Length


class Register(FlaskForm):
    first_name = StringField(
        "First Name",
        validators=[
            DataRequired(),
            Length(min=3, max=32)
        ],
        render_kw={"placeholder": "First Name"}
    )
    last_name = StringField(
        "Last Name",
        validators=[
            DataRequired(),
            Length(min=3, max=32)
        ],
        render_kw={"placeholder": "Last Name"}
    )
    email = EmailField(
        "Email",
        validators=[
            DataRequired(),
            Length(max=32),
        ],
        render_kw={"placeholder": "Email"}
    )
    verify_email = EmailField(
        "Email",
        validators=[
            DataRequired(),
            EqualTo("email")
        ],
        render_kw={"placeholder": "Verify Email"}
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8)
        ],
        render_kw={"placeholder": "Password"}
    )
    verify_password = PasswordField(
        "Verify Password",
        validators=[
            DataRequired(),
            EqualTo("password")
        ],
        render_kw={"placeholder": "Verify Password"}
    )
    submit = SubmitField("Create Account")

    def validate_email(self, email: EmailField):
        if db.session.execute(
            db.select(User)
            .filter_by(email=email.data)
        ).first():
            raise ValidationError("User with this email already exists")


class Login(FlaskForm):
    email = EmailField(
        "Email",
        validators=[
            DataRequired(),
            Length(max=32),
        ],
        render_kw={"placeholder": "Email"}
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8)
        ],
        render_kw={"placeholder": "Password"}
    )
    submit = SubmitField("Login")


class ForgotPassword(FlaskForm):
    email = EmailField(
        "Email",
        validators=[
            DataRequired(),
            Length(min=8)
        ],
        render_kw={"placeholder": "Email"}
    )
    submit = SubmitField("Request Password Reset")

    def validate_email(self, email: EmailField):
        user = db.session.execute(
            db.select(User).filter_by(email=email.data)
        ).first()

        if not user:
            raise ValidationError("Invalid email")


class Reset(FlaskForm):
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8)
        ],
        render_kw={"placeholder": "New Password"}
    )
    verify_password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            EqualTo("password")
        ],
        render_kw={"placeholder": "Verify Password"}
    )
    submit = SubmitField("Reset Password")
