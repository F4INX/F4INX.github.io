#!/bin/bash
# Run LinkChecker locally.
# Replaces PLACEHOLDER in .linkcheckerrc with the script directory path.
# Usage: ./linkchecker.sh [output.log] [--ignored ignored-urls.log]
# If output file is given, output is redirected there.
# If --ignored is given, a list of ignored/filtered URLs is written to that file.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG="$SCRIPT_DIR/.linkcheckerrc"
CONFIG_TMP="$(mktemp)"
PUBLIC_DIR="$SCRIPT_DIR/public"
OUTPUT_FILE=""
IGNORED_FILE=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --ignored)
            IGNORED_FILE="$2"
            shift 2
            ;;
        *)
            OUTPUT_FILE="$1"
            shift
            ;;
    esac
done

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

VERBOSE=""
if [ -n "$IGNORED_FILE" ]; then
    VERBOSE="-v --no-status"
fi

if [ -n "$OUTPUT_FILE" ]; then
    linkchecker --config "$CONFIG_TMP" \
        --check-extern --no-warnings $VERBOSE \
        "$PUBLIC_DIR/" > "$OUTPUT_FILE" 2>&1
    echo "Output written to $OUTPUT_FILE"
    echo "Errors: $(grep -c 'Result.*Error' "$OUTPUT_FILE")"
else
    linkchecker --config "$CONFIG_TMP" \
        --check-extern --no-warnings $VERBOSE \
        "$PUBLIC_DIR/"
fi

if [ -n "$IGNORED_FILE" ]; then
    if [ -n "$OUTPUT_FILE" ]; then
        grep -B5 "Result.*ignored\|Result.*filtered" "$OUTPUT_FILE" \
            | sed 's/\x1b\[[0-9;]*m//g' \
            | grep "Real URL" \
            | sed 's/^Real URL   //' \
            | sort -u > "$IGNORED_FILE"
    else
        echo "Error: --ignored requires an output file to be specified first." >&2
        rm -f "$CONFIG_TMP"
        exit 1
    fi
    echo "Ignored URLs written to $IGNORED_FILE"
    echo "Ignored: $(wc -l < "$IGNORED_FILE")"
fi

rm -f "$CONFIG_TMP"
