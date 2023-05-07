#!/bin/bash
set -e
set -x

# Check if the number of arguments is correct
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 SQLITE_PATH LOG_PATH"
    exit 1
fi

SQLITE_PATH="$1"
LOG_PATH="$2"

mkdir -p "$SQLITE_PATH" "$LOG_PATH"

if [ -f "$SQLITE_PATH/api.db" ]; then
    echo "deleting db"
    rm "$SQLITE_PATH/api.db"
fi
if [ -f "$LOG_PATH/log.log" ]; then
    echo "deleting log"
    rm "$LOG_PATH/log.log"
fi
