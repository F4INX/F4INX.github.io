#!/bin/bash
# Shared functions for running LinkChecker.
# Sourced by linkchecker.sh (local) and scripts/run-linkchecker-ci.sh (CI).

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

# Run LinkChecker and write output to a log file (text) and CSV file.
# Usage: run_linkchecker <config> <public_dir> <text_logfile> <csv_file>
run_linkchecker() {
    local config="$1"
    local public_dir="$2"
    local text_logfile="$3"
    local csv_file="$4"

    linkchecker --config "$config" \
        --check-extern --no-warnings -v --no-status \
        -F "csv/utf-8/$csv_file" \
        "$public_dir/" > "$text_logfile" 2>&1
}

# Print formatted summary to stdout.
# Usage: print_summary <text_logfile> <csv_file> [silent_ignore_file]
print_summary() {
    local text_logfile="$1"
    local csv_file="$2"
    local silent_ignore="${3:-}"

    echo "## Link Checker Results"
    echo ""

    # Status table
    _print_status_table "$text_logfile" "$csv_file"
    echo ""

    # Errors
    local has_errors
    has_errors="$(grep -c "Result.*Error" "$text_logfile" || true)"
    if [ "$has_errors" -gt 0 ]; then
        echo "### Errors"
        echo ""
        grep -B5 "Result.*Error" "$text_logfile" \
            | sed 's/\x1b\[[0-9;]*m//g' \
            | grep "Real URL\|Result" \
            | sed 's/^Real URL   /URL: /;s/^Result     /  /'
        echo ""
    fi

    # Redirects
    _print_redirects "$csv_file"
    echo ""

    # Ignored links
    echo "### Ignored links (manual check recommended)"
    echo ""
    _extract_ignored_urls "$csv_file" "- " "$silent_ignore"
    echo ""

    # Stats
    grep "That's it" "$text_logfile" | sed 's/\x1b\[[0-9;]*m//g' || true
}

# Internal: print status table from log and CSV.
# Usage: _print_status_table <text_logfile> <csv_file>
_print_status_table() {
    local text_logfile="$1"
    local csv_file="$2"

    local total errors redirects ignored filtered warnings
    total="$(grep "That's it" "$text_logfile" | sed 's/\x1b\[[0-9;]*m//g' | grep -oP '\d+ links' | grep -oP '^\d+')"
    errors="$(grep -c "Result.*Error" "$text_logfile" || true)"
    redirects="$(_count_csv "$csv_file" "warningstring" "Redirected")"
    ignored="$(_count_csv "$csv_file" "warningstring" "ignored" "exact")"
    filtered="$(_count_csv "$csv_file" "result" "filtered" "exact")"
    warnings="$(grep "That's it" "$text_logfile" | sed 's/\x1b\[[0-9;]*m//g' | grep -oP '\d+ warnings' | grep -oP '^\d+')"

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

# Internal: count rows in CSV matching a field value.
# Usage: _count_csv <csv_file> <field> <pattern> [exact]
_count_csv() {
    local csv_file="$1"
    local field="$2"
    local pattern="$3"
    local mode="${4:-}"

    python3 -c "
import csv
with open('$csv_file') as f:
    lines = [l for l in f if not l.startswith('#')]
    reader = csv.DictReader(lines, delimiter=';')
    count = 0
    for r in reader:
        val = r.get('$field', '')
        if '$mode' == 'exact':
            if val == '$pattern':
                count += 1
        else:
            if '$pattern' in val:
                count += 1
    print(count)
" 2>/dev/null || echo 0
}

# Internal: print redirects from CSV.
# Usage: _print_redirects <csv_file>
_print_redirects() {
    local csv_file="$1"

    python3 -c "
import csv
with open('$csv_file') as f:
    lines = [l for l in f if not l.startswith('#')]
    reader = csv.DictReader(lines, delimiter=';')
    for r in reader:
        ws = r.get('warningstring', '')
        if 'Redirected' in ws:
            url = r.get('urlname', '')
            real = r.get('url', '')
            if url and real and url != real:
                print(f'- {url} --> {real}')
" 2>/dev/null
}

# Internal: extract ignored/filtered URLs from CSV.
# Usage: _extract_ignored_urls <csv_file> <prefix> [silent_ignore_file]
_extract_ignored_urls() {
    local csv_file="$1"
    local prefix="$2"
    local silent_ignore="${3:-}"

    local result
    result="$(python3 -c "
import csv
with open('$csv_file') as f:
    lines = [l for l in f if not l.startswith('#')]
    reader = csv.DictReader(lines, delimiter=';')
    for r in reader:
        ws = r.get('warningstring', '')
        res = r.get('result', '')
        if ws == 'ignored' or res == 'filtered':
            url = r.get('url', '')
            if url:
                print(f'$prefix{url}')
" 2>/dev/null | sort -u)"

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
# Usage: extract_ignored <csv_file> <output_file> [silent_ignore_file]
extract_ignored() {
    local csv_file="$1"
    local output_file="$2"
    local silent_ignore="${3:-}"

    _extract_ignored_urls "$csv_file" "" "$silent_ignore" > "$output_file"
}
