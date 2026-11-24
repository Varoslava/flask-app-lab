from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    BooleanField,
    SelectField,
    SelectMultipleField,
    SubmitField
)
from wtforms.fields import DateTimeLocalField
from wtforms.validators import DataRequired, Length

from app.extensions import db
from app.users.models import User
from app.posts.models import Tag


class PostForm(FlaskForm):
    title = StringField(
        "Заголовок",
        validators=[DataRequired(message="Введіть заголовок."), Length(max=150)]
    )
    content = TextAreaField(
        "Текст поста",
        validators=[DataRequired(message="Введіть текст поста.")]
    )
    enabled = BooleanField("Активний пост", default=True)
    publish_date = DateTimeLocalField(
        "Дата та час публікації",
        format="%Y-%m-%dT%H:%M",
        validators=[DataRequired(message="Оберіть дату та час.")]
    )
    category = SelectField(
        "Категорія",
        choices=[
            ("news", "Новини"),
            ("publication", "Публікація"),
            ("tech", "Технології"),
            ("other", "Інше")
        ],
        validators=[DataRequired(message="Оберіть категорію.")]
    )
    user_id = SelectField(
        "Автор",
        coerce=int,
        validators=[DataRequired(message="Оберіть автора.")]
    )
    tags = SelectMultipleField(
        "Теги",
        coerce=int
    )
    submit = SubmitField("Зберегти")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        users = db.session.scalars(
            db.select(User).order_by(User.username)
        ).all()

        self.user_id.choices = [
            (user.id, user.username) for user in users
        ]

        tags = db.session.scalars(
            db.select(Tag).order_by(Tag.name)
        ).all()

        self.tags.choices = [
            (tag.id, tag.name) for tag in tags
        ]


class DeletePostForm(FlaskForm):
    submit = SubmitField("Так, видалити пост")