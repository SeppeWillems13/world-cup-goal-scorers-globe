#!/bin/bash

# Install required packages
pip install -r requirements.txt

# Set environment variables
export STREAMLIT_SERVER_PORT=8080
export STREAMLIT_SERVER_HEADLESS=true
