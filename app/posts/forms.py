from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.fields import DateTimeLocalField
from wtforms.validators import DataRequired, Length


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
    submit = SubmitField("Зберегти")


class DeletePostForm(FlaskForm):
    submit = SubmitField("Так, видалити пост")
