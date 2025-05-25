#!/bin/bash

# Colors
GREEN="\e[0;32m"
RESET="\e[0m"

# Gunicorn Parameters
WORKERS=4
BIND="0.0.0.0"
PORT=5000

usage() {
    cat << EOF
Usage: $0 [options]

Options:
    -w, --workers WORKERS   Number of Gunicorn workers (default: $WORKERS)
    -b, --bind IP_ADDRESS   Bind address (default: $BIND)
    -p, --port PORT         Specify the port to run on (default: $PORT)
    -h, --help              Show this help message
EOF
    exit 0
}

while [[ $# -gt 0 ]]; do
    case $1 in
        -w | --workers)
            WORKERS=$2
            shift 2
            ;;
        -b | --bind)
            BIND=$2
            shift 2
            ;;
        -p | --port)
            PORT=$2
            shift 2
            ;;
        -h | --help)
            usage
            ;;
        *)
            echo "Unknown option: $1"
            usage
            ;;
    esac
done

echo -e "[${GREEN}+${RESET}] ${GREEN}Initializing Database...${RESET}"
uv run python init_db.py
echo -e "[${GREEN}+${RESET}] ${GREEN}Running Gunicorn with ${WORKERS} workers...${RESET}"
uv run gunicorn -w $WORKERS -b $BIND:$PORT main:app
