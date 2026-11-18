"""Insert data into products table

Revision ID: 688d4e533248
Revises: f56f07f0273c
Create Date: 2026-11-18 14:27:31.139367

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision = '688d4e533248'
down_revision = 'f56f07f0273c'
branch_labels = None
depends_on = None


def upgrade():
    categories_table = table(
        "categories",
        column("id", sa.Integer),
        column("name", sa.String)
    )

    products_table = table(
        "products",
        column("name", sa.String),
        column("price", sa.Float),
        column("active", sa.Boolean),
        column("category_id", sa.Integer)
    )

    op.bulk_insert(categories_table, [
        {"id": 2, "name": "Electronics"},
        {"id": 3, "name": "Books"},
        {"id": 4, "name": "Clothing"}
    ])

    op.bulk_insert(products_table, [
        {
            "name": "Laptop",
            "price": 1200.0,
            "active": True,
            "category_id": 2
        },
        {
            "name": "Smartphone LG",
            "price": 800.0,
            "active": True,
            "category_id": 2
        },
        {
            "name": "Novel",
            "price": 20.0,
            "active": True,
            "category_id": 3
        },
        {
            "name": "T-Shirt",
            "price": 25.0,
            "active": False,
            "category_id": 4
        }
    ])


def downgrade():
    op.execute("""
        DELETE FROM products
        WHERE name IN ('Laptop', 'Smartphone LG', 'Novel', 'T-Shirt');
    """)

    op.execute("""
        DELETE FROM categories
        WHERE id IN (2, 3, 4);
    """)