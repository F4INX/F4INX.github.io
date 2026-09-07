#!/bin/bash
# Run LinkChecker locally.
# Usage: ./linkchecker.sh [output.log] [--ignored ignored-urls.log]
# If output file is given, LinkChecker output is saved there.
# If --ignored is given, a list of ignored/filtered URLs is written to that file.
# A formatted summary is always printed to stdout.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/scripts/linkchecker-common.sh"

CONFIG="$SCRIPT_DIR/.linkcheckerrc"
PUBLIC_DIR="$SCRIPT_DIR/public"
SILENT_IGNORE="$SCRIPT_DIR/linkchecker-silent-ignore"
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

if [ ! -d "$PUBLIC_DIR" ]; then
    echo "Building site..."
    hugo --minify --baseURL "https://f4inx.github.io/" --cwd "$SCRIPT_DIR"
fi

# Prepare config and run
CONFIG_TMP="$(prepare_config "$CONFIG" "$PUBLIC_DIR")"
LOGFILE="$(mktemp)"
CSV_FILE="$(mktemp)"
run_linkchecker "$CONFIG_TMP" "$PUBLIC_DIR" "$LOGFILE" "$CSV_FILE"

# Copy raw output if requested
if [ -n "$OUTPUT_FILE" ]; then
    cp "$LOGFILE" "$OUTPUT_FILE"
    echo "Output written to $OUTPUT_FILE"
fi

# Print summary to stdout
print_summary "$LOGFILE" "$CSV_FILE" "$SILENT_IGNORE"

# Extract ignored URLs if requested
if [ -n "$IGNORED_FILE" ]; then
    extract_ignored "$CSV_FILE" "$IGNORED_FILE" "$SILENT_IGNORE"
    echo "Ignored URLs written to $IGNORED_FILE"
    echo "Ignored: $(wc -l < "$IGNORED_FILE")"
fi

# Cleanup
rm -f "$CONFIG_TMP" "$LOGFILE" "$CSV_FILE"
