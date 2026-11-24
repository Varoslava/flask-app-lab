from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(db.String(80), nullable=False)
    email: Mapped[str] = mapped_column(db.String(120), nullable=False)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)

    posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="user",
        cascade="all, delete-orphan"
    )