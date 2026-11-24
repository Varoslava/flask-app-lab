from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_login import UserMixin

from app.extensions import db, bcrypt


class User(UserMixin, db.Model):
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

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)