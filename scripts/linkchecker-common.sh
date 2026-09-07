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

    # Status table
    _print_status_table "$logfile"
    echo ""

    # Errors
    local has_errors
    has_errors="$(grep -c "Result.*Error" "$logfile" || true)"
    if [ "$has_errors" -gt 0 ]; then
        echo "### Errors"
        echo ""
        grep -B5 "Result.*Error" "$logfile" \
            | strip_ansi \
            | grep "Real URL\|Result" \
            | sed 's/^Real URL   /URL: /;s/^Result     /  /'
        echo ""
    fi

    # Redirects
    local has_redirects
    has_redirects="$(grep -c "http-redirected" "$logfile" || true)"
    if [ "$has_redirects" -gt 0 ]; then
        echo "### Redirects"
        echo ""
        _print_redirects "$logfile"
        echo ""
    fi

    # Ignored links
    echo "### Ignored links (manual check recommended)"
    echo ""
    _extract_ignored_urls "$logfile" "- " "$silent_ignore"
    echo ""

    # Stats
    grep "That's it" "$logfile" | strip_ansi || true
}

# Internal: print status table from log.
# Usage: _print_status_table <logfile>
_print_status_table() {
    local logfile="$1"

    local total errors redirects ignored filtered
    total="$(grep "That's it" "$logfile" | sed 's/\x1b\[[0-9;]*m//g' | grep -oP '\d+ links' | grep -oP '^\d+')"
    errors="$(grep -c "Result.*Error" "$logfile" || true)"
    redirects="$(grep -c "http-redirected" "$logfile" || true)"
    ignored="$(grep -c "Result.*ignored" "$logfile" || true)"
    filtered="$(grep -c "Result.*filtered" "$logfile" || true)"

    local warnings
    warnings="$(grep "That's it" "$logfile" | sed 's/\x1b\[[0-9;]*m//g' | grep -oP '\d+ warnings' | grep -oP '^\d+')"

    local ok
    ok=$((total - errors - redirects - ignored - filtered))

    echo "| Status        | Count |"
    echo "|---------------|-------|"
    echo "| Total         | $total |"
    echo "| OK            | $ok |"
    echo "| Redirects     | $redirects |"
    echo "| Filtered      | $filtered |"
    echo "| Ignored       | $ignored |"
    echo "| Warnings      | $warnings |"
    echo "| Errors        | $errors |"
}

# Internal: print redirects from log.
# Usage: _print_redirects <logfile>
_print_redirects() {
    local logfile="$1"

    # LinkChecker logs redirects with [http-redirected] warnings.
    # We extract the original URL and the final Real URL.
    awk '
    /^URL / {
        if (url != "" && real != "" && redirected) {
            print "- " url " --> " real
        }
        url=$0; sub(/^URL        `/, "", url); sub(/.$/, "", url);
        real=""; redirected=0
    }
    /\[http-redirected\]/ { redirected=1 }
    /^Real URL / {
        real=$0; sub(/^Real URL   /, "", real)
    }
    /^Result/ {
        if (url != "" && real != "" && redirected) {
            print "- " url " --> " real
        }
        url=""; real=""; redirected=0
    }
    ' "$logfile"
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
