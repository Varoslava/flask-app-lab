from pathlib import Path
from datetime import datetime
from tinydb import TinyDB
import atexit

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

db = TinyDB(DATA_DIR / "products.json", encoding="utf-8")
products_table = db.table("products")
atexit.register(db.close)

CATEGORY_MAPPING = {
    "Електроніка": "electronics",
    "Одяг": "clothing",
    "Продукти": "food",
    "Інше": "other"
}


def normalize_categories():
    for product in products_table.all():
        category = product.get("category")

        if category in CATEGORY_MAPPING:
            products_table.update(
                {"category": CATEGORY_MAPPING[category]},
                doc_ids=[product.doc_id]
            )


def seed_products():
    if not products_table.all():
        products_table.insert_multiple([
            {
                "id": 1,
                "name": "Laptop",
                "price": 1200.00,
                "content": (
                    "Потужний ноутбук з процесором Intel Core i7, "
                    "16 ГБ оперативної пам’яті та SSD на 512 ГБ."
                ),
                "category": "electronics",
                "quantity": 1,
                "image": None,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            {
                "id": 2,
                "name": "Phone",
                "price": 800.00,
                "content": (
                    "Смартфон із 6.5-дюймовим OLED-дисплеєм, "
                    "подвійною камерою та акумулятором на 5000 мА·год."
                ),
                "category": "electronics",
                "quantity": 1,
                "image": None,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            {
                "id": 3,
                "name": "PC",
                "price": 1800.00,
                "content": (
                    "Настільний комп’ютер для ігор або роботи "
                    "з графікою: RTX 4070, 32 ГБ RAM, 1 ТБ SSD."
                ),
                "category": "electronics",
                "quantity": 1,
                "image": None,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        ])