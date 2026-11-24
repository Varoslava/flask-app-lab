from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db


post_tags = db.Table(
    "post_tags",
    db.Column(
        "post_id",
        db.Integer,
        db.ForeignKey("post.id"),
        primary_key=True
    ),
    db.Column(
        "tag_id",
        db.Integer,
        db.ForeignKey("tags.id"),
        primary_key=True
    )
)


class Post(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(db.String(150), nullable=False)
    content: Mapped[str] = mapped_column(db.Text, nullable=False)
    posted: Mapped[datetime] = mapped_column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )
    category: Mapped[str] = mapped_column(
        db.Enum("news", "publication", "tech", "other", name="post_category"),
        nullable=False,
        default="other"
    )
    is_active: Mapped[bool] = mapped_column(
        db.Boolean,
        nullable=False,
        default=True
    )
    user_id: Mapped[int | None] = mapped_column(
        db.ForeignKey("users.id"),
        nullable=True
    )

    user: Mapped["User | None"] = relationship(
        "User",
        back_populates="posts"
    )

    tags: Mapped[list["Tag"]] = relationship(
        "Tag",
        secondary=post_tags,
        back_populates="posts"
    )

    def __repr__(self):
        return f"<Post {self.id}: {self.title}>"


class Tag(db.Model):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(
        db.String(50),
        unique=True,
        nullable=False
    )

    posts: Mapped[list["Post"]] = relationship(
        "Post",
        secondary=post_tags,
        back_populates="tags"
    )

    def __repr__(self):
        return f"<Tag {self.name}>"