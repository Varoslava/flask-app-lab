import logging
from pathlib import Path
from flask import render_template, request, redirect, url_for, flash
from app import app
from app.forms import ContactForm

portfolio = {
    "name": "Зорій Ярослава-Іванна Василівна",
    "short_name": "Ярослава-Іванна Зорій",
    "group": "ІПЗ-32",
    "specialty": "Інженерія програмного забезпечення",
    "role": "Студентка та майбутня розробниця",
    "university": "Прикарпатський національний університет імені Василя Стефаника",
    "course": "3 курс",
    "about": (
        "Я навчаюся на спеціальності «Інженерія програмного "
        "забезпечення». Цікавлюся програмуванням, веброзробкою "
        "та сучасними інформаційними технологіями. "
        "Мені подобається створювати власні проєкти, "
        "працювати з кодом та здобувати практичні навички."
    ),
    "skills": [
        "Створення вебсторінок",
        "Основи програмування",
        "Робота з Git та GitHub",
        "Робота з базами даних",
        "Командна робота",
        "Самостійне навчання"
    ],
    "technologies": [
        "Python",
        "Flask",
        "HTML5",
        "CSS3",
        "Bootstrap",
        "JavaScript",
        "Git",
        "GitHub",
        "SQL"
    ],
    "projects": [
        {
            "name": "Перший Flask-проєкт",
            "description": (
                "Навчальний вебзастосунок на Python "
                "із використанням Flask, GitHub та Render."
            ),
            "stack": "Python · Flask · GitHub"
        },
        {
            "name": "Персональне портфоліо",
            "description": (
                "Адаптивний сайт із резюме, контактами "
                "та шаблонами Jinja2. Створений під час "
                "виконання лабораторної роботи №2."
            ),
            "stack": "Flask · HTML · CSS · Bootstrap"
        }
    ],
    "github": "https://github.com/Varoslava",
    "email": "yaroslava-ivanna.zorii.24@pnu.edu.ua"
}

log_dir = Path(app.root_path).parent / "logs"
log_dir.mkdir(exist_ok=True)

contact_logger = logging.getLogger("contact_messages")
contact_logger.setLevel(logging.INFO)
contact_logger.propagate = False

if not contact_logger.handlers:
    handler = logging.FileHandler(
        log_dir / "contacts.log",
        encoding="utf-8"
    )
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(message)s")
    )
    contact_logger.addHandler(handler)

@app.route("/")
def resume():
    return render_template(
        "resume.html",
        title="Резюме",
        person=portfolio
    )


@app.route("/contacts", methods=["GET", "POST"])
def contacts():
    form = ContactForm()

    if form.validate_on_submit():
        contact_logger.info(
            "Name: %s | Email: %s | Subject: %s | Message: %s",
            form.name.data,
            form.email.data,
            form.subject.data,
            form.message.data
        )

        flash("Ваше повідомлення успішно надіслано!", "success")
        return redirect(url_for("contacts"))

    if request.method == "POST":
        flash("Не вдалося надіслати повідомлення. Перевірте правильність заповнення форми.", "danger")

    return render_template(
        "contacts.html",
        title="Контакти",
        person=portfolio,
        form=form
    )


@app.route("/homepage")
def home():
    return render_template(
        "homepage.html",
        title="Головна сторінка",
        person=portfolio
    )