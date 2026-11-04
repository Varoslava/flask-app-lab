from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, DecimalField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class ProductForm(FlaskForm):
    name = StringField(
        "Назва товару",
        validators=[
            DataRequired(message="Введіть назву товару."),
            Length(min=3, max=100, message="Назва має містити від 3 до 100 символів.")
        ]
    )

    content = TextAreaField(
        "Опис товару",
        validators=[
            DataRequired(message="Введіть опис товару.")
        ]
    )

    price = DecimalField(
        "Ціна",
        places=2,
        validators=[
            DataRequired(message="Введіть ціну."),
            NumberRange(min=0.01, message="Ціна повинна бути більшою за 0.")
        ]
    )

    category = SelectField(
        "Категорія",
        choices=[
            ("electronics", "Електроніка"),
            ("clothing", "Одяг"),
            ("food", "Продукти"),
            ("other", "Інше")
        ],
        validators=[DataRequired(message="Оберіть категорію.")]
    )

    quantity = IntegerField(
        "Кількість",
        validators=[
            DataRequired(message="Введіть кількість."),
            NumberRange(min=0, message="Кількість не може бути від'ємною.")
        ]
    )

    image = FileField(
        "Зображення",
        validators=[
            FileAllowed(["jpg", "jpeg", "png"], "Дозволені формати: JPG, JPEG, PNG.")
        ]
    )

    submit = SubmitField("Додати товар")

class DeleteProductForm(FlaskForm):
    submit = SubmitField("Видалити")