#!/bin/bash

python3 -m venv /app/cuu-illegal-waste-venv
source /app/cuu-illegal-waste-venv/bin/activate
pip3 install -r /app/workflows/requirements.txt
