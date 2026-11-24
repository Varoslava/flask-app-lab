from flask import render_template, request, redirect, url_for, flash, make_response
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)
from sqlalchemy import or_

from app.extensions import db
from app.users import users_bp
from app.users.models import User
from app.users.forms import RegistrationForm, LoginForm


@users_bp.route("/hi/<name>")
def greetings(name):
    age = request.args.get("age")

    return render_template(
        "users/hi.html",
        title="Користувачі",
        name=name.upper(),
        age=age
    )


@users_bp.route("/admin")
def admin():
    return redirect(
        url_for(
            "users.greetings",
            name="Administrator",
            age=45
        )
    )


@users_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("users.profile"))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(
            username=form.username.data.strip(),
            email=form.email.data.strip().lower()
        )

        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        login_user(user)

        flash("Реєстрація успішна! Ви автоматично увійшли в систему.", "success")
        return redirect(url_for("users.profile"))

    return render_template(
        "users/register.html",
        title="Реєстрація",
        form=form
    )


@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("users.profile"))

    form = LoginForm()

    if form.validate_on_submit():
        identifier = form.username.data.strip()

        user = User.query.filter(
            or_(
                User.username == identifier,
                User.email == identifier.lower()
            )
        ).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Ви успішно увійшли в систему!", "success")

            next_page = request.args.get("next")

            if next_page and next_page.startswith("/") and not next_page.startswith("//"):
                return redirect(next_page)

            return redirect(url_for("users.profile"))

        flash("Неправильний логін або пароль.", "danger")

    return render_template(
        "login.html",
        title="Вхід",
        form=form
    )


@users_bp.route("/profile")
@users_bp.route("/account")
@login_required
def profile():
    theme = request.cookies.get("theme", "light")

    visit_cookie = f"visit_count_{current_user.id}"
    visit_count = request.cookies.get(visit_cookie, "0")

    try:
        visit_count = int(visit_count) + 1
    except (ValueError, TypeError):
        visit_count = 1

    response = make_response(
        render_template(
            "profile.html",
            title="Мій профіль",
            username=current_user.username,
            email=current_user.email,
            theme=theme,
            visit_count=visit_count,
            cookies=request.cookies.items()
        )
    )

    response.set_cookie(
        visit_cookie,
        str(visit_count),
        max_age=30 * 24 * 60 * 60
    )

    return response


@users_bp.route("/all-users")
@login_required
def all_users():
    users = User.query.order_by(User.id.asc()).all()

    return render_template(
        "users/all_users.html",
        title="Усі користувачі",
        users=users,
        users_count=len(users)
    )


@users_bp.route("/set-theme/<theme>")
@login_required
def set_theme(theme):
    if theme not in ("light", "dark"):
        flash("Невідома тема оформлення.", "danger")
        return redirect(url_for("users.profile"))

    response = make_response(redirect(url_for("users.profile")))
    response.set_cookie("theme", theme, max_age=30 * 24 * 60 * 60)

    return response


@users_bp.route("/add-cookie", methods=["POST"])
@login_required
def add_cookie():
    key = request.form.get("key", "").strip()
    value = request.form.get("value", "")
    max_age = request.form.get("max_age", "3600").strip()

    if not key or key.lower() == "session":
        flash("Введіть коректний ключ cookie.", "danger")
        return redirect(url_for("users.profile"))

    try:
        max_age = int(max_age)

        if max_age <= 0:
            raise ValueError
    except ValueError:
        flash("Термін дії має бути додатним числом секунд.", "danger")
        return redirect(url_for("users.profile"))

    response = make_response(redirect(url_for("users.profile")))
    response.set_cookie(key, value, max_age=max_age)
    flash(f"Cookie «{key}» успішно додано.", "success")

    return response


@users_bp.route("/delete-cookie", methods=["POST"])
@login_required
def delete_cookie():
    key = request.form.get("key", "").strip()

    response = make_response(redirect(url_for("users.profile")))

    if key == "__all__":
        for cookie_key in request.cookies:
            response.delete_cookie(cookie_key)

        flash("Усі cookies видалено.", "success")

    elif key:
        if key in request.cookies:
            response.delete_cookie(key)
            flash(f"Cookie «{key}» успішно видалено.", "success")
        else:
            flash(f"Cookie «{key}» не знайдено.", "danger")
    else:
        flash("Вкажіть ключ cookie для видалення.", "danger")

    return response


@users_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("Ви вийшли із системи.", "success")

    return redirect(url_for("users.login"))