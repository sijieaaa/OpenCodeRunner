#!/bin/bash

# Switch to the directory of the script
cd "$(dirname "$0")"

# Start FastAPI server
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
