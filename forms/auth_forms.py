
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    EqualTo
)


class RegistrationForm(FlaskForm):

    username = StringField(
        "Full Name",
        validators=[
            DataRequired(),
            Length(min=3, max=80)
        ]
    )

    email = StringField(
        "Email Address",
        validators=[
            DataRequired(),
            Email(),
            Length(max=120)
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8, message="Password must contain at least 8 characters.")
        ]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords do not match.")
        ]
    )

    submit = SubmitField("Create Account")


class LoginForm(FlaskForm):

    email = StringField(
        "Email Address",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField("Sign In")
