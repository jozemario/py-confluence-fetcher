#!/bin/bash
#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Use the desired Python version
PYENV_VERSION="3.9.5"

# Activate pyenv and set the Python version
eval "$(pyenv init --path)"
pyenv local $PYENV_VERSION

# Create a virtual environment

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pre-commit install
