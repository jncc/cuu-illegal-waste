#!/bin/bash

virtualenv -p python3 /app/cuu-illegal-waste-venv
source /app/cuu-illegal-waste-venv/bin/activate
pip install -r /app/workflows/requirements.txt
