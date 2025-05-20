#!/bin/bash

# Colors
GREEN="\e[0;32m"
RESET="\e[0m"

# Gunicorn Parameters
WORKERS=4
PORT=5000

echo -e "[${GREEN}+${RESET}] ${GREEN}Initializing Database...${RESET}"
uv run python init_db.py
echo -e "[${GREEN}+${RESET}] ${GREEN}Running Gunicorn...${RESET}"
uv run gunicorn -w $WORKERS -b 0.0.0.0:$PORT main:app
