#!/bin/bash
# Shared functions for running LinkChecker.
# Sourced by linkchecker.sh (local) and scripts/run-linkchecker-ci.sh (CI).

# Strip ANSI color codes from input.
strip_ansi() {
    sed 's/\x1b\[[0-9;]*m//g'
}

# Prepare LinkChecker config by replacing the PLACEHOLDER with the given public dir.
# Usage: prepare_config <config_file> <public_dir>
# Outputs the temp config path to stdout.
prepare_config() {
    local config="$1"
    local public_dir="$2"
    local config_tmp
    config_tmp="$(mktemp)"

    local webroot
    webroot="file://$(echo "$public_dir" | sed 's/ /%20/g')/"
    sed "s|file:///PLACEHOLDER/|$webroot|" "$config" > "$config_tmp"

    echo "$config_tmp"
}

# Run LinkChecker and write output to a log file.
# Usage: run_linkchecker <config> <public_dir> <logfile>
run_linkchecker() {
    local config="$1"
    local public_dir="$2"
    local logfile="$3"

    linkchecker --config "$config" \
        --check-extern --no-warnings -v --no-status \
        "$public_dir/" > "$logfile" 2>&1
}

# Print formatted summary to stdout.
# Usage: print_summary <logfile> [silent_ignore_file]
print_summary() {
    local logfile="$1"
    local silent_ignore="${2:-}"

    echo "## Link Checker Results"
    echo ""

    # Errors
    local has_errors
    has_errors="$(grep -c "Result.*Error" "$logfile" || true)"
    if [ "$has_errors" -gt 0 ]; then
        grep -B5 "Result.*Error" "$logfile" \
            | strip_ansi \
            | grep "Real URL\|Result" \
            | sed 's/^Real URL   /URL: /;s/^Result     /  /'
    else
        echo "No errors found."
    fi
    echo ""

    # Ignored links
    echo "### Ignored links (manual check recommended)"
    echo ""
    _extract_ignored_urls "$logfile" "- " "$silent_ignore"
    echo ""

    # Stats
    grep "That's it" "$logfile" | strip_ansi || true
}

# Internal: extract ignored/filtered URLs from log.
# Usage: _extract_ignored_urls <logfile> <prefix> [silent_ignore_file]
_extract_ignored_urls() {
    local logfile="$1"
    local prefix="$2"
    local silent_ignore="${3:-}"

    local result
    result="$(grep -B5 "Result.*ignored\|Result.*filtered" "$logfile" \
        | strip_ansi \
        | grep "Real URL" \
        | sed "s/^Real URL   /$prefix/" \
        | sort -u)"

    if [ -n "$silent_ignore" ] && [ -f "$silent_ignore" ]; then
        local silent_tmp
        silent_tmp="$(mktemp)"
        grep -v '^#' "$silent_ignore" | grep -v '^[[:space:]]*$' > "$silent_tmp"
        result="$(echo "$result" | grep -Ev -f "$silent_tmp")"
        rm -f "$silent_tmp"
    fi

    echo "$result"
}

# Extract ignored URLs to a file.
# Usage: extract_ignored <logfile> <output_file> [silent_ignore_file]
extract_ignored() {
    local logfile="$1"
    local output_file="$2"
    local silent_ignore="${3:-}"

    _extract_ignored_urls "$logfile" "" "$silent_ignore" > "$output_file"
}
