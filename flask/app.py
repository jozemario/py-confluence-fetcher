from dotenv import load_dotenv
from flask import Flask, jsonify, request
from confluence.client import Confluence
from confluence.models.content import ContentType
import os

load_dotenv()

app = Flask(__name__)

# Confluence configuration
CONFLUENCE_URL = os.environ.get("CONFLUENCE_URL")
CONFLUENCE_USERNAME = os.environ.get("CONFLUENCE_USERNAME")
CONFLUENCE_PASSWORD = os.environ.get("CONFLUENCE_PASSWORD")


@app.route("/spaces", methods=["GET"])
def get_spaces():
    with Confluence(CONFLUENCE_URL, (CONFLUENCE_USERNAME, CONFLUENCE_PASSWORD)) as c:
        spaces = c.get_spaces()
        return spaces


@app.route("/pages/<page_id>", methods=["GET"])
def get_page_content(page_id):
    try:
        with Confluence(
            CONFLUENCE_URL, (CONFLUENCE_USERNAME, CONFLUENCE_PASSWORD)
        ) as c:
            page = c.get_content_by_id(page_id, expand=["body.storage"])
            return jsonify(
                {
                    "id": page.id,
                    "type": page.type,
                    "title": page.title,
                    "body": page.body.storage.value,
                }
            )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/pages", methods=["POST"])
def create_page():
    try:
        space_key = request.json["space_key"]
        title = request.json["title"]
        body = request.json["body"]

        with Confluence(
            CONFLUENCE_URL, (CONFLUENCE_USERNAME, CONFLUENCE_PASSWORD)
        ) as c:
            created_page = c.create_content(ContentType.PAGE, title, space_key, body)
            return (
                jsonify(
                    {
                        "id": created_page.id,
                        "title": created_page.title,
                        "type": created_page.type,
                    }
                ),
                201,
            )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run()
