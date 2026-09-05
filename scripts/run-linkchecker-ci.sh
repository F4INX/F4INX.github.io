#!/bin/bash
# CI script to run LinkChecker and produce a GitHub Actions summary.
# Used by .github/workflows/link-check.yml

set -e

# Replace PLACEHOLDER with the CI workspace path
sed -i "s|file:///PLACEHOLDER/|file://$GITHUB_WORKSPACE/public/|" .linkcheckerrc

linkchecker --config .linkcheckerrc \
  --check-extern --no-warnings -v --no-status \
  ./public/ > linkchecker-output.log 2>&1

# Print summary
echo "## Link Checker Results" >> $GITHUB_STEP_SUMMARY
echo "" >> $GITHUB_STEP_SUMMARY
grep -B5 "Result.*Error" linkchecker-output.log \
  | sed 's/\x1b\[[0-9;]*m//g' \
  | grep "Real URL\|Result" \
  | sed 's/^Real URL   /URL: /;s/^Result     /  /' \
  >> $GITHUB_STEP_SUMMARY
echo "" >> $GITHUB_STEP_SUMMARY

# Print ignored links summary
echo "### Ignored links (manual check recommended)" >> $GITHUB_STEP_SUMMARY
echo "" >> $GITHUB_STEP_SUMMARY
grep -B5 "Result.*ignored\|Result.*filtered" linkchecker-output.log \
  | sed 's/\x1b\[[0-9;]*m//g' \
  | grep "Real URL" \
  | sed 's/^Real URL   /- /' \
  | sort -u >> $GITHUB_STEP_SUMMARY
echo "" >> $GITHUB_STEP_SUMMARY

# Print stats
grep "That's it" linkchecker-output.log >> $GITHUB_STEP_SUMMARY
