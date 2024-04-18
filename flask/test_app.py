import unittest
from unittest.mock import patch
from app import app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @patch("app.confluence.get_spaces")
    def test_get_spaces(self, mock_get_spaces):
        mock_space = type("Space", (), {"name": "Test Space"})
        mock_get_spaces.return_value = [mock_space]

        response = self.client.get("/spaces")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, ["Test Space"])

    @patch("app.confluence.create_page")
    def test_create_page(self, mock_create_page):
        mock_page = type("Page", (), {"id": "123", "title": "Test Page"})
        mock_create_page.return_value = mock_page

        payload = {
            "space_key": "TEST",
            "title": "Test Page",
            "body": "This is a test page.",
        }

        response = self.client.post("/pages", json=payload)
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {"id": "123", "title": "Test Page"})


if __name__ == "__main__":
    unittest.main()
