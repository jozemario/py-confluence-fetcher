import pytest
from httpx import AsyncClient
from app import app


@pytest.mark.asyncio
async def test_get_spaces(mocker):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        mock_response = [{"name": "Test Space"}]
        mocker.patch(
            "confluence.client.Confluence.get_spaces", return_value=mock_response
        )

        response = await ac.get("/rest/spaces")
        print(response.json())
        assert response.status_code == 200
        assert response.json() == mock_response


@pytest.mark.asyncio
async def test_create_page(mocker):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        mock_response = {"id": "123", "title": "Test Page"}
        mock_confluence_instance = mocker.MagicMock()
        mock_confluence_instance.create_page.return_value = type(
            "Page", (), mock_response
        )
        mocker.patch(
            "confluence.client.Confluence.__enter__",
            return_value=mock_confluence_instance,
        )
        mocker.patch("confluence.client.Confluence.__exit__")

        payload = {
            "space_key": "TEST",
            "title": "Test Page",
            "body": "This is a test page.",
        }

        response = await ac.post("/pages", json=payload)
        assert response.status_code == 201
        assert response.json() == {"id": "123", "title": "Test Page"}
