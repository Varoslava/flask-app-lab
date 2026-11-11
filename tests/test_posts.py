import unittest
from app import create_app
from app.extensions import db
from app.posts.models import Post


class PostsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        post = Post(
            title="Перший тестовий пост",
            content="Текст для перевірки роботи постів.",
            category="news",
            author="Test Author"
        )
        db.session.add(post)
        db.session.commit()
        self.post_id = post.id

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_posts_list(self):
        response = self.client.get("/post")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Перший тестовий пост".encode(), response.data)

    def test_post_detail(self):
        response = self.client.get(f"/post/{self.post_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Текст для перевірки".encode(), response.data)

    def test_create_post(self):
        response = self.client.post("/post/create", data={
            "title": "Новий пост",
            "content": "Текст нового поста для тестування.",
            "publish_date": "2026-11-11T12:30",
            "category": "tech",
            "enabled": "y",
            "submit": "Зберегти"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(db.session.scalar(db.select(Post).where(Post.title == "Новий пост")))

    def test_update_post(self):
        response = self.client.post(f"/post/{self.post_id}/update", data={
            "title": "Оновлений заголовок",
            "content": "Оновлений текст поста.",
            "publish_date": "2026-11-11T13:00",
            "category": "publication",
            "enabled": "y",
            "submit": "Зберегти зміни"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        post = db.session.get(Post, self.post_id)
        self.assertEqual(post.title, "Оновлений заголовок")

    def test_delete_post(self):
        response = self.client.post(f"/post/{self.post_id}/delete", data={"submit": "Так, видалити пост"}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(db.session.get(Post, self.post_id))

    def test_post_not_found(self):
        response = self.client.get("/post/999")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
