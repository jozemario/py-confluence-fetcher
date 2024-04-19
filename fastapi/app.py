from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from confluence.client import Confluence
import os

load_dotenv()

app = FastAPI()

# Confluence configuration
CONFLUENCE_URL = os.environ.get("CONFLUENCE_URL")
CONFLUENCE_USERNAME = os.environ.get("CONFLUENCE_USERNAME")
CONFLUENCE_PASSWORD = os.environ.get("CONFLUENCE_PASSWORD")


class PageCreate(BaseModel):
    space_key: str
    title: str
    body: str


@app.get("/rest/spaces")
async def get_spaces():
    with Confluence(CONFLUENCE_URL, (CONFLUENCE_USERNAME, CONFLUENCE_PASSWORD)) as c:
        spaces = c.get_spaces()
        # return [space.name for space in spaces]
        return spaces


@app.post("/pages", status_code=201)
async def create_page(page: PageCreate):
    try:
        with Confluence(
            CONFLUENCE_URL, (CONFLUENCE_USERNAME, CONFLUENCE_PASSWORD)
        ) as c:
            created_page = c.create_page(
                space_key=page.space_key, title=page.title, body=page.body
            )
            return {"id": created_page.id, "title": created_page.title}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
