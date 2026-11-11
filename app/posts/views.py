from datetime import datetime
from flask import render_template, redirect, url_for, flash, session
from app.extensions import db
from app.posts import posts_bp
from app.posts.forms import PostForm, DeletePostForm
from app.posts.models import Post


@posts_bp.route("")
def all_posts():
    statement = (
        db.select(Post)
        .where(Post.is_active.is_(True))
        .order_by(Post.posted.desc())
    )
    posts = db.session.scalars(statement).all()
    return render_template("posts/posts.html", title="Усі пости", posts=posts)


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
        form.publish_date.data = datetime.now().replace(second=0, microsecond=0)
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            posted=form.publish_date.data,
            category=form.category.data,
            is_active=form.enabled.data,
            author=session.get("username", "Anonymous")
        )
        db.session.add(post)
        db.session.commit()
        flash("Пост успішно створено!", "success")
        return redirect(url_for("posts.detail_post", id=post.id))
    return render_template("posts/add_post.html", title="Створити пост", form=form)


@posts_bp.route("/<int:id>/update", methods=["GET", "POST"])
def update_post(id):
    post = db.get_or_404(Post, id)
    form = PostForm(obj=post)
    if not form.is_submitted():
        form.publish_date.data = post.posted
        form.enabled.data = post.is_active
    if form.validate_on_submit():
        form.populate_obj(post)
        post.posted = form.publish_date.data
        post.is_active = form.enabled.data
        post.author = post.author or session.get("username", "Anonymous")
        db.session.commit()
        flash("Пост успішно оновлено!", "success")
        return redirect(url_for("posts.detail_post", id=post.id))
    form.submit.label.text = "Зберегти зміни"
    return render_template("posts/add_post.html", title="Редагувати пост", form=form, post=post)


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
