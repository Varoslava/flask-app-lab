import unittest

from app import create_app
from app.extensions import db
from app.users.models import User


class AuthTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def create_user(self):
        user = User(
            username="testuser",
            email="test@example.com"
        )
        user.set_password("TestPassword123")

        db.session.add(user)
        db.session.commit()

        return user

    def test_registration_page(self):
        response = self.client.get("/users/register")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Реєстрація".encode(), response.data)

    def test_login_page(self):
        response = self.client.get("/users/login")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Увійти".encode(), response.data)

    def test_user_registration(self):
        response = self.client.post(
            "/users/register",
            data={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "NewPassword123",
                "confirm_password": "NewPassword123",
                "submit": "Зареєструватися"
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)

        user = db.session.scalar(
            db.select(User).where(User.email == "newuser@example.com")
        )

        self.assertIsNotNone(user)
        self.assertEqual(user.username, "newuser")
        self.assertNotEqual(user.password, "NewPassword123")
        self.assertTrue(user.check_password("NewPassword123"))

    def test_login_success(self):
        self.create_user()

        response = self.client.post(
            "/users/login",
            data={
                "username": "testuser",
                "password": "TestPassword123",
                "submit": "Увійти"
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("testuser".encode(), response.data)

    def test_login_wrong_password(self):
        self.create_user()

        response = self.client.post(
            "/users/login",
            data={
                "username": "testuser",
                "password": "WrongPassword123",
                "submit": "Увійти"
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Неправильний логін або пароль.".encode(),
            response.data
        )

    def test_logout(self):
        self.create_user()

        self.client.post(
            "/users/login",
            data={
                "username": "testuser",
                "password": "TestPassword123",
                "submit": "Увійти"
            }
        )

        response = self.client.post(
            "/users/logout",
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Ви вийшли із системи.".encode(), response.data)

    def test_profile_requires_login(self):
        response = self.client.get("/users/profile")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/users/login", response.location)

    def test_all_users_requires_login(self):
        response = self.client.get("/users/all-users")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/users/login", response.location)


if __name__ == "__main__":
    unittest.main()