from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class ContactForm(FlaskForm):
    name = StringField(
        "Ваше ім'я",
        validators=[
            DataRequired(message="Введіть ваше ім'я."),
            Length(min=2, max=100, message="Ім'я має містити від 2 до 100 символів.")
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Введіть email."),
            Email(message="Введіть коректну email-адресу.")
        ]
    )

    subject = SelectField(
        "Тема повідомлення",
        choices=[
            ("question", "Запитання"),
            ("cooperation", "Співпраця"),
            ("suggestion", "Пропозиція"),
            ("other", "Інше")
        ],
        validators=[
            DataRequired(message="Оберіть тему повідомлення.")
        ]
    )

    message = TextAreaField(
        "Повідомлення",
        validators=[
            DataRequired(message="Введіть текст повідомлення."),
            Length(min=10, max=2000, message="Повідомлення має містити від 10 до 2000 символів.")
        ]
    )

    submit = SubmitField("Надіслати повідомлення")