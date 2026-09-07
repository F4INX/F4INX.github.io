#!/bin/bash
# CI script to run LinkChecker and produce a GitHub Actions summary.
# Used by .github/workflows/link-check.yml

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/linkchecker-common.sh"

CONFIG="$GITHUB_WORKSPACE/.linkcheckerrc"
PUBLIC_DIR="$GITHUB_WORKSPACE/public"
SILENT_IGNORE="$GITHUB_WORKSPACE/linkchecker-silent-ignore"
LOGFILE="$GITHUB_WORKSPACE/linkchecker-output.log"

# Prepare config and run
CONFIG_TMP="$(prepare_config "$CONFIG" "$PUBLIC_DIR")"
# LinkChecker returns non-zero when it finds errors/warnings; don't fail the script
run_linkchecker "$CONFIG_TMP" "$PUBLIC_DIR" "$LOGFILE" || true

# Print summary to GitHub Actions step summary
print_summary "$LOGFILE" "$SILENT_IGNORE" | tee -a "$GITHUB_STEP_SUMMARY"

# Cleanup
rm -f "$CONFIG_TMP"
