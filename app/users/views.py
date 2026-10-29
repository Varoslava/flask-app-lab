from flask import render_template, request, redirect, url_for, session, flash, make_response
from app.users import users_bp


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


@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if username == "admin" and password == "12345":
            session["username"] = username
            flash("Ви успішно увійшли в систему!", "success")
            return redirect(url_for("users.profile"))

        flash("Неправильний логін або пароль.", "error")

    return render_template("login.html", title="Вхід")


@users_bp.route("/profile")
def profile():
    if "username" not in session:
        flash("Спочатку увійдіть у систему.", "error")
        return redirect(url_for("users.login"))

    theme = request.cookies.get("theme", "light")
    visit_count = request.cookies.get("visit_count", "0")

    try:
        visit_count = int(visit_count) + 1
    except ValueError:
        visit_count = 1

    response = make_response(
        render_template(
            "profile.html",
            title="Мій профіль",
            username=session["username"],
            theme=theme,
            visit_count=visit_count,
            cookies=request.cookies.items()
        )
    )

    response.set_cookie("visit_count", str(visit_count), max_age=30 * 24 * 60 * 60)

    return response


@users_bp.route("/set-theme/<theme>")
def set_theme(theme):
    if "username" not in session:
        flash("Спочатку увійдіть у систему.", "error")
        return redirect(url_for("users.login"))

    if theme not in ("light", "dark"):
        flash("Невідома тема оформлення.", "error")
        return redirect(url_for("users.profile"))

    response = make_response(redirect(url_for("users.profile")))
    response.set_cookie("theme", theme, max_age=30 * 24 * 60 * 60)

    return response



@users_bp.route("/add-cookie", methods=["POST"])
def add_cookie():
    if "username" not in session:
        flash("Спочатку увійдіть у систему.", "error")
        return redirect(url_for("users.login"))

    key = request.form.get("key", "").strip()
    value = request.form.get("value", "")
    max_age = request.form.get("max_age", "3600").strip()

    if not key or key.lower() == "session":
        flash("Введіть коректний ключ cookie.", "error")
        return redirect(url_for("users.profile"))

    try:
        max_age = int(max_age)
        if max_age <= 0:
            raise ValueError
    except ValueError:
        flash("Термін дії має бути додатним числом секунд.", "error")
        return redirect(url_for("users.profile"))

    response = make_response(redirect(url_for("users.profile")))
    response.set_cookie(key, value, max_age=max_age)
    flash(f"Cookie «{key}» успішно додано.", "success")

    return response


@users_bp.route("/delete-cookie", methods=["POST"])
def delete_cookie():
    if "username" not in session:
        flash("Спочатку увійдіть у систему.", "error")
        return redirect(url_for("users.login"))

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
            flash(f"Cookie «{key}» не знайдено.", "error")
    else:
        flash("Вкажіть ключ cookie для видалення.", "error")

    return response


@users_bp.route("/logout")
def logout():
    session.pop("username", None)
    flash("Ви вийшли із системи.", "success")
    return redirect(url_for("users.login"))