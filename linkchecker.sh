#!/bin/bash
# Run LinkChecker locally.
# Replaces PLACEHOLDER in .linkcheckerrc with the script directory path.
# Usage: ./linkchecker.sh [output.log]
# If output file is given, output is redirected there.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG="$SCRIPT_DIR/.linkcheckerrc"
CONFIG_TMP="$(mktemp)"
PUBLIC_DIR="$SCRIPT_DIR/public"

if [ ! -f "$CONFIG" ]; then
    echo "Error: $CONFIG not found."
    exit 1
fi

# Replace PLACEHOLDER with the local public/ path (URL-encoded)
WEBROOT="file://$(echo "$PUBLIC_DIR" | sed 's/ /%20/g')/"
sed "s|file:///PLACEHOLDER/|$WEBROOT|" "$CONFIG" > "$CONFIG_TMP"

if [ ! -d "$PUBLIC_DIR" ]; then
    echo "Building site..."
    hugo --minify --baseURL "https://f4inx.github.io/" --cwd "$SCRIPT_DIR"
fi

if [ -n "$1" ]; then
    linkchecker --config "$CONFIG_TMP" \
        --check-extern --no-warnings \
        "$PUBLIC_DIR/" > "$1" 2>&1
    echo "Output written to $1"
    echo "Errors: $(grep -c 'Result.*Error' "$1")"
else
    linkchecker --config "$CONFIG_TMP" \
        --check-extern --no-warnings \
        "$PUBLIC_DIR/"
fi

rm -f "$CONFIG_TMP"
