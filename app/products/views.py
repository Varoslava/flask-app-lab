from flask import render_template, abort, redirect, url_for, flash
from app.products import products_bp
from app.products.database import (
    products_table,
    seed_products,
    normalize_categories
)
from app.products.forms import ProductForm, DeleteProductForm
from datetime import datetime
import uuid
from pathlib import Path
from werkzeug.utils import secure_filename
from tinydb import where

seed_products()
normalize_categories()

UPLOAD_FOLDER = Path(__file__).resolve().parent / "static" / "uploads"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)


@products_bp.route("/")
def product_list():
    products = products_table.all()

    return render_template(
        "products/products.html",
        title="Список товарів",
        products=products
    )


@products_bp.route("/<int:product_id>")
def product_detail(product_id):
    product = next(
        (
            item for item in products_table.all()
            if item["id"] == product_id
        ),
        None
    )

    if product is None:
        abort(404)

    return render_template(
        "products/detail_product.html",
        title=product["name"],
        product=product,
        delete_form=DeleteProductForm()
    )

@products_bp.route("/add", methods=["GET", "POST"])
def product_add():
    form = ProductForm()

    if form.validate_on_submit():
        products = products_table.all()
        new_id = max(
            (product["id"] for product in products),
            default=0
        ) + 1

        image_filename = None

        if form.image.data:
            image = form.image.data
            extension = Path(secure_filename(image.filename)).suffix.lower()
            image_filename = f"{uuid.uuid4().hex}{extension}"
            image.save(UPLOAD_FOLDER / image_filename)

        product = {
            "id": new_id,
            "name": form.name.data,
            "content": form.content.data,
            "price": float(form.price.data),
            "category": form.category.data,
            "quantity": form.quantity.data,
            "image": image_filename,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        products_table.insert(product)

        flash("Товар успішно додано!", "success")
        return redirect(
            url_for("products.product_detail", product_id=new_id)
        )

    return render_template(
        "products/product_form.html",
        title="Додавання товару",
        form=form
    )

@products_bp.route("/<int:product_id>/edit", methods=["GET", "POST"])
def product_edit(product_id):
    product = products_table.get(where("id") == product_id)

    if product is None:
        abort(404)

    form = ProductForm()

    if form.validate_on_submit():
        update_data = {
            "name": form.name.data,
            "content": form.content.data,
            "price": float(form.price.data),
            "category": form.category.data,
            "quantity": form.quantity.data
        }

        new_image = None

        if form.image.data:
            image = form.image.data
            extension = Path(secure_filename(image.filename)).suffix.lower()
            new_image = f"{uuid.uuid4().hex}{extension}"
            image.save(UPLOAD_FOLDER / new_image)
            update_data["image"] = new_image

        products_table.update(
            update_data,
            doc_ids=[product.doc_id]
        )

        if new_image and product.get("image"):
            old_image_path = UPLOAD_FOLDER / product["image"]

            if old_image_path.exists():
                old_image_path.unlink()

        flash("Товар успішно оновлено!", "success")
        return redirect(
            url_for("products.product_detail", product_id=product_id)
        )

    if not form.is_submitted():
        form.name.data = product["name"]
        form.content.data = product["content"]
        form.price.data = product["price"]
        form.category.data = product["category"]
        form.quantity.data = product["quantity"]

    form.submit.label.text = "Зберегти зміни"

    return render_template(
        "products/product_form.html",
        title="Редагування товару",
        form=form
    )

@products_bp.route("/<int:product_id>/delete", methods=["POST"])
def product_delete(product_id):
    product = products_table.get(where("id") == product_id)

    if product is None:
        abort(404)

    if product.get("image"):
        image_path = UPLOAD_FOLDER / product["image"]

        if image_path.exists():
            image_path.unlink()

    products_table.remove(doc_ids=[product.doc_id])

    flash("Товар успішно видалено!", "success")
    return redirect(url_for("products.product_list"))