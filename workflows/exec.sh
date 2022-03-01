#!/bin/bash
umask 002
source /app/cuu-illegal-waste-venv/bin/activate
cd /app/workflows
LUIGI_CONFIG_PATH='/app/workflows/luigi.cfg' PYTHONPATH='.' luigi --module process_slc_pair "$@" --local-scheduler
python /app/CopyState.py
