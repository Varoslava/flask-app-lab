from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db

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
    author: Mapped[str] = mapped_column(
        db.String(20),
        nullable=False,
        default="Anonymous"
    )

    def __repr__(self):
        return f"<Post {self.id}: {self.title}>"