from fastapi.testclient import TestClient
from unittest.mock import patch
from app import app

client = TestClient(app)


@patch("app.confluence.get_spaces")
def test_get_spaces(mock_get_spaces):
    mock_space = type("Space", (), {"name": "Test Space"})
    mock_get_spaces.return_value = [mock_space]

    response = client.get("/spaces")
    assert response.status_code == 200
    assert response.json() == ["Test Space"]


@patch("app.confluence.create_page")
def test_create_page(mock_create_page):
    mock_page = type("Page", (), {"id": "123", "title": "Test Page"})
    mock_create_page.return_value = mock_page

    payload = {
        "space_key": "TEST",
        "title": "Test Page",
        "body": "This is a test page.",
    }

    response = client.post("/pages", json=payload)
    assert response.status_code == 201
    assert response.json() == {"id": "123", "title": "Test Page"}
