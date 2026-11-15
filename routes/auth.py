
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request
)

from flask_login import login_user, logout_user, current_user

from urllib.parse import urlparse, urljoin

from models import db, User
from forms.auth_forms import RegistrationForm, LoginForm


auth = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)


def is_safe_url(target):

    if not target:
        return False

    host_url = urlparse(request.host_url)
    redirect_url = urlparse(urljoin(request.host_url, target))

    return (
        redirect_url.scheme in ("http", "https")
        and host_url.netloc == redirect_url.netloc
    )


@auth.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    form = RegistrationForm()

    if form.validate_on_submit():

        email = form.email.data.strip().lower()
        username = form.username.data.strip()

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:
            flash(
                "An account with this email already exists.",
                "danger"
            )

            return render_template(
                "auth/register.html",
                form=form
            )

        user = User(
            username=username,
            email=email
        )

        user.set_password(form.password.data)

        try:
            db.session.add(user)
            db.session.commit()

            login_user(user)

            flash(
                "Your account has been created successfully!",
                "success"
            )

            return redirect(url_for("dashboard"))

        except Exception:
            db.session.rollback()

            flash(
                "Something went wrong. Please try again.",
                "danger"
            )

    return render_template(
        "auth/register.html",
        form=form
    )


@auth.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    form = LoginForm()

    if form.validate_on_submit():

        email = form.email.data.strip().lower()

        user = User.query.filter_by(
            email=email
        ).first()

        if user and user.check_password(form.password.data):

            login_user(user)

            flash(
                f"Welcome back, {user.username}!",
                "success"
            )

            next_page = request.args.get("next")

            if is_safe_url(next_page):
                return redirect(next_page)

            return redirect(url_for("dashboard"))

        flash(
            "Invalid email address or password.",
            "danger"
        )

    return render_template(
        "auth/login.html",
        form=form
    )


@auth.route("/logout", methods=["POST"])
def logout():

    if current_user.is_authenticated:
        logout_user()

        flash(
            "You have been logged out successfully.",
            "success"
        )

    return redirect(url_for("auth.login"))
