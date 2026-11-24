from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    EqualTo,
    ValidationError
)

from app.users.models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        "Логін",
        validators=[
            DataRequired(message="Введіть логін."),
            Length(min=3, max=80, message="Логін повинен містити від 3 до 80 символів.")
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Введіть email."),
            Email(message="Введіть коректну email-адресу."),
            Length(max=120)
        ]
    )

    password = PasswordField(
        "Пароль",
        validators=[
            DataRequired(message="Введіть пароль."),
            Length(min=8, message="Пароль повинен містити щонайменше 8 символів.")
        ]
    )

    confirm_password = PasswordField(
        "Підтвердження пароля",
        validators=[
            DataRequired(message="Підтвердіть пароль."),
            EqualTo("password", message="Паролі не збігаються.")
        ]
    )

    submit = SubmitField("Зареєструватися")

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data.strip()).first()

        if user:
            raise ValidationError("Цей логін уже використовується.")


    def validate_email(self, field):
        email = field.data.strip().lower()

        if "@" in email:
            domain = email.rsplit("@", 1)[1]

            if "." not in domain or len(domain.rsplit(".", 1)[-1]) < 2:
                raise ValidationError("Введіть коректну електронну адресу.")

        user = User.query.filter_by(email=email).first()

        if user:
            raise ValidationError("Користувач із таким email уже зареєстрований.")


class LoginForm(FlaskForm):
    username = StringField(
        "Логін або email",
        validators=[DataRequired(message="Введіть логін або email.")]
    )

    password = PasswordField(
        "Пароль",
        validators=[DataRequired(message="Введіть пароль.")]
    )

    submit = SubmitField("Увійти")