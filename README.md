# py-confluence fetcher poc
```
project/
  ├── .pre-commit-config.yaml
  ├── requirements.txt
  ├── setup.sh
  ├── fastapi/
  │   ├── app.py
  │   └── test_app.py
  └── flask/
      ├── app.py
      └── test_app.py
```
Now, to set up the project:

Navigate to the project root directory.
Run the setup.sh script to create a virtual environment, install dependencies, and set up pre-commit hooks:



```bash
chmod +x setup.sh

./setup.sh
```
Activate the virtual environment:

```bash
source venv/bin/activate
```
Run the apps:

For FastAPI:
```bash
python fastapi/app.py
```

For Flask:
```bash
python flask/app.py
```
Run the tests:

For FastAPI:

```bash
pytest fastapi/test_app.py
```

For Flask:

```bash
python flask/test_app.py
```
With this setup, the pre-commit hooks will run for both the FastAPI and Flask applications when you commit changes from the project root directory. The hooks will only apply to files within the respective directories.