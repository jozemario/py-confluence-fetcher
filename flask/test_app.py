import pytest
from httpx import AsyncClient
from confluence.models.content import Content
from app import app


@pytest.mark.asyncio
async def test_get_page_content(mocker):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        mock_response = {
            "id": "123",
            "type": "page",
            "title": "Test Page",
            "body": {
                "storage": {
                    "value": "<p>This is the page content.</p>",
                    "representation": "storage",
                }
            },
        }
        mock_confluence_instance = mocker.MagicMock()
        mock_confluence_instance.get_content_by_id.return_value = type(
            "Page", (), mock_response
        )
        mocker.patch(
            "confluence.client.Confluence.__enter__",
            return_value=mock_confluence_instance,
        )
        mocker.patch("confluence.client.Confluence.__exit__")

        response = await ac.get("/pages/123")
        assert response.status_code == 200
        assert response.json() == {
            "id": "123",
            "type": "page",
            "title": "Test Page",
            "body": "<p>This is the page content.</p>",
        }


@pytest.mark.asyncio
async def test_create_page(mocker):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        mock_response = {"id": "123", "title": "New Page", "type": "page"}
        mock_confluence_instance = mocker.MagicMock()
        mock_confluence_instance.create_content.return_value = type(
            "Page", (), mock_response
        )
        mocker.patch(
            "confluence.client.Confluence.__enter__",
            return_value=mock_confluence_instance,
        )
        mocker.patch("confluence.client.Confluence.__exit__")

        payload = {
            "space_key": "TEST",
            "title": "New Page",
            "body": "This is a new page.",
        }

        response = await ac.post("/pages", json=payload)
        assert response.status_code == 201
        assert response.json() == {"id": "123", "title": "New Page", "type": "page"}


def test_create_with_minimal_json():
    p = Content({"id": 1, "title": "Hello", "status": "current", "type": "page"})
    assert str(p) == "1 - Hello"


def test_create_complete():
    p = Content(
        {
            "id": "65577",
            "type": "page",
            "status": "current",
            "title": "SandBox",
            "space": {"id": 98306, "key": "SAN", "name": "SandBox", "type": "global"},
            "history": {
                "latest": True,
                "createdBy": {
                    "type": "anonymous",
                    "profilePicture": {
                        "path": "anonymous.png",
                        "width": 48,
                        "height": 48,
                        "isDefault": True,
                    },
                    "displayName": "Anonymous",
                },
                "createdDate": "2017-09-22T11:03:07.420+01:00",
            },
            "version": {
                "by": {
                    "type": "known",
                    "username": "user",
                    "userKey": "12345",
                    "profilePicture": {
                        "path": "default.png",
                        "width": 48,
                        "height": 48,
                        "isDefault": True,
                    },
                    "displayName": "user",
                },
                "when": "2017-10-28T17:05:56.026+01:00",
                "message": "",
                "number": 8,
                "minorEdit": False,
                "hidden": False,
            },
            "body": {
                "storage": {
                    "value": "",
                    "representation": "storage",
                    "_expandable": {"content": "/rest/api/content/65577"},
                }
            },
            "metadata": {},
            "extensions": {"position": "none"},
        }
    )
    assert p.body.storage == ""
    assert p.body.storage_representation == "storage"
    assert not hasattr(p.body, "edit")
    assert p.history.latest
    assert p.space.id == 98306
