from datetime import datetime

from flask import render_template, redirect, url_for, flash

from app.extensions import db
from app.posts import posts_bp
from app.posts.forms import PostForm, DeletePostForm
from app.posts.models import Post, Tag


@posts_bp.route("")
def all_posts():
    statement = (
        db.select(Post)
        .where(Post.is_active.is_(True))
        .order_by(Post.posted.desc())
    )
    posts = db.session.scalars(statement).all()

    return render_template(
        "posts/posts.html",
        title="Усі пости",
        posts=posts
    )


@posts_bp.route("/<int:id>")
def detail_post(id):
    post = db.get_or_404(Post, id)

    return render_template(
        "posts/detail_post.html",
        title=post.title,
        post=post,
        delete_form=DeletePostForm()
    )


@posts_bp.route("/create", methods=["GET", "POST"])
def create_post():
    form = PostForm()

    if not form.is_submitted():
        form.publish_date.data = datetime.now().replace(
            second=0,
            microsecond=0
        )

    if form.validate_on_submit():
        selected_tags = db.session.scalars(
            db.select(Tag).where(Tag.id.in_(form.tags.data))
        ).all() if form.tags.data else []

        post = Post(
            title=form.title.data,
            content=form.content.data,
            posted=form.publish_date.data,
            category=form.category.data,
            is_active=form.enabled.data,
            user_id=form.user_id.data,
            tags=selected_tags
        )

        db.session.add(post)
        db.session.commit()

        flash("Пост успішно створено!", "success")
        return redirect(url_for("posts.detail_post", id=post.id))

    return render_template(
        "posts/add_post.html",
        title="Створити пост",
        form=form
    )


@posts_bp.route("/<int:id>/update", methods=["GET", "POST"])
def update_post(id):
    post = db.get_or_404(Post, id)
    form = PostForm(obj=post)

    if not form.is_submitted():
        form.publish_date.data = post.posted
        form.enabled.data = post.is_active
        form.tags.data = [tag.id for tag in post.tags]

    if form.validate_on_submit():
        selected_tags = db.session.scalars(
            db.select(Tag).where(Tag.id.in_(form.tags.data))
        ).all() if form.tags.data else []

        post.title = form.title.data
        post.content = form.content.data
        post.posted = form.publish_date.data
        post.category = form.category.data
        post.is_active = form.enabled.data
        post.user_id = form.user_id.data
        post.tags = selected_tags

        db.session.commit()

        flash("Пост успішно оновлено!", "success")
        return redirect(url_for("posts.detail_post", id=post.id))

    form.submit.label.text = "Зберегти зміни"

    return render_template(
        "posts/add_post.html",
        title="Редагувати пост",
        form=form,
        post=post
    )


@posts_bp.route("/<int:id>/delete", methods=["GET", "POST"])
def delete_post(id):
    post = db.get_or_404(Post, id)
    form = DeletePostForm()

    if form.validate_on_submit():
        db.session.delete(post)
        db.session.commit()

        flash("Пост успішно видалено!", "success")
        return redirect(url_for("posts.all_posts"))

    return render_template(
        "posts/delete_confirm.html",
        title="Підтвердження видалення",
        post=post,
        form=form
    )