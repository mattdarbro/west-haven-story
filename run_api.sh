#!/bin/bash
# Run the Storyteller API server

# Activate virtual environment
source venv/bin/activate

# Set PYTHONPATH to project root
export PYTHONPATH=/Users/mattdarbro/Desktop/Story

# Run the API
python backend/api/main.py
