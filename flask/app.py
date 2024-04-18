# app.py
from flask import Flask, jsonify, request
from confluence import Confluence
import os

app = Flask(__name__)

# Confluence configuration
CONFLUENCE_URL = os.environ.get('CONFLUENCE_URL')
CONFLUENCE_USERNAME = os.environ.get('CONFLUENCE_USERNAME')
CONFLUENCE_PASSWORD = os.environ.get('CONFLUENCE_PASSWORD')

confluence = Confluence(
    url=CONFLUENCE_URL,
    username=CONFLUENCE_USERNAME,
    password=CONFLUENCE_PASSWORD
)

@app.route('/spaces', methods=['GET'])
def get_spaces():
    spaces = confluence.get_spaces()
    return jsonify([space.name for space in spaces])

@app.route('/pages', methods=['POST'])
def create_page():
    space_key = request.json['space_key']
    title = request.json['title']
    body = request.json['body']

    page = confluence.create_page(
        space_key=space_key,
        title=title,
        body=body
    )

    return jsonify({'id': page.id, 'title': page.title})

if __name__ == '__main__':
    app.run()