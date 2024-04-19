import os


class Config:
    CONFLUENCE_URL = os.environ.get("CONFLUENCE_URL")
    CONFLUENCE_USERNAME = os.environ.get("CONFLUENCE_USERNAME")
    CONFLUENCE_PASSWORD = os.environ.get("CONFLUENCE_PASSWORD")
