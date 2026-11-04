
import unittest
import tempfile
from pathlib import Path
from tinydb import TinyDB

from app import app
from app.products import views as product_views


class FlaskProductsTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False

        self.client = app.test_client()

        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_db = TinyDB(
            Path(self.temp_dir.name) / "test_products.json"
        )
        self.test_products_table = self.test_db.table("products")

        self.original_table = product_views.products_table
        product_views.products_table = self.test_products_table

        self.test_products_table.insert({
            "id": 1,
            "name": "Test Laptop",
            "price": 1200.00,
            "content": "Тестовий опис ноутбука.",
            "category": "electronics",
            "quantity": 5,
            "image": None,
            "created_at": "2026-11-04 12:00:00"
        })

    def tearDown(self):
        product_views.products_table = self.original_table
        self.test_db.close()
        self.temp_dir.cleanup()

    def test_products_page(self):
        response = self.client.get("/products/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Laptop", response.data)

    def test_product_detail(self):
        response = self.client.get("/products/1")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Laptop", response.data)

    def test_product_not_found(self):
        response = self.client.get("/products/999")

        self.assertEqual(response.status_code, 404)

    def test_add_product(self):
        response = self.client.post(
            "/products/add",
            data={
                "name": "Test Phone",
                "content": "Тестовий опис телефону.",
                "price": "800.00",
                "category": "electronics",
                "quantity": "3"
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.test_products_table.all()), 2)

        product = self.test_products_table.get(
            lambda item: item["name"] == "Test Phone"
        )
        self.assertIsNotNone(product)

    def test_edit_product(self):
        response = self.client.post(
            "/products/1/edit",
            data={
                "name": "Updated Laptop",
                "content": "Оновлений опис ноутбука.",
                "price": "1500.00",
                "category": "electronics",
                "quantity": "7"
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)

        product = self.test_products_table.get(
            lambda item: item["id"] == 1
        )
        self.assertEqual(product["name"], "Updated Laptop")
        self.assertEqual(product["price"], 1500.00)

    def test_delete_product(self):
        response = self.client.post(
            "/products/1/delete",
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.test_products_table.all()), 0)

    def test_add_product_invalid_data(self):
        response = self.client.post(
            "/products/add",
            data={
                "name": "A",
                "content": "",
                "price": "-10",
                "category": "electronics",
                "quantity": "-1"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.test_products_table.all()), 1)

    def test_edit_product_not_found(self):
        response = self.client.get("/products/999/edit")
        self.assertEqual(response.status_code, 404)

    def test_delete_product_not_found(self):
        response = self.client.post("/products/999/delete")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
