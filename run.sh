#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

RT_DIR=".vault"
ARCHIVE="vault/data/core.pkg"

if [ ! -f "$RT_DIR/bin/python3" ]; then
    if [ -f "$ARCHIVE" ]; then
        mkdir -p "$RT_DIR"
        unzip -q "$ARCHIVE" -d "$RT_DIR"
    fi
fi

if [ -f "$RT_DIR/bin/python3" ]; then
    "$RT_DIR/bin/python3" main.py
else
    python3 main.py
fi
