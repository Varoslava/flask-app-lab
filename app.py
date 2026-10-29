
from flask import Flask, render_template, request

app = Flask(__name__)

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


@app.route("/")
def resume():
    return render_template(
        "resume.html",
        title="Резюме",
        person=portfolio
    )


@app.route("/contacts", methods=["GET", "POST"])
def contacts():
    submitted = request.method == "POST"

    return render_template(
        "contacts.html",
        title="Контакти",
        person=portfolio,
        submitted=submitted
    )


if __name__ == "__main__":
    app.run(debug=True)
