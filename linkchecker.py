#!/usr/bin/env python3
"""Run LinkChecker and produce a formatted summary.

Usage:
    ./linkchecker.py [output.log] [--ignored ignored-urls.log]
    ./linkchecker.py --ci
"""

import argparse
import csv
import os
import re
import subprocess
import sys
import tempfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

ANSI_RE = re.compile(r'\x1b\[[0-9;]*m')


def strip_ansi(text):
    """Remove ANSI SGR escape codes from linkchecker's text output.

    LinkChecker emits color codes (e.g. \\x1b[31m for red) even when
    writing to a pipe rather than a TTY. This is only needed when parsing
    the text output for the link count cross-check; CSV output contains
    no ANSI codes.
    """
    return ANSI_RE.sub('', text)


def prepare_config(config_path, public_dir, output_path):
    """Replace PLACEHOLDER in config and write the result to output_path."""
    webroot = 'file://' + public_dir.replace(' ', '%20') + '/'
    with open(config_path) as f:
        content = f.read()
    content = content.replace('file:///PLACEHOLDER/', webroot)
    with open(output_path, 'w') as f:
        f.write(content)


def run_linkchecker(config, public_dir, csv_file):
    """Run LinkChecker, return captured stdout and write CSV file.

    LinkChecker exits non-zero when:
      - invalid links were found (expected, this is what we check for)
      - warnings were found with warnings enabled (disabled via --no-warnings)
      - a program error occurred (e.g. bad config, missing binary)

    Since we cannot distinguish "found broken links" from "program error"
    by exit code alone, we check whether the CSV file was actually written.
    An empty or missing CSV means LinkChecker itself failed.
    """
    result = subprocess.run(
        [
            'linkchecker', '--config', config,
            '--check-extern', '--no-warnings', '-v', '--no-status',
            '-F', f'csv/utf-8/{csv_file}',
            public_dir + '/',
        ],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
    )
    if not os.path.isfile(csv_file) or os.path.getsize(csv_file) == 0:
        raise RuntimeError(
            f'LinkChecker did not produce CSV output (exit code {result.returncode}).\n'
            f'{result.stdout}'
        )
    return result.stdout


def parse_csv(csv_file):
    """Parse CSV, skip comment lines, return list of row dicts."""
    with open(csv_file, encoding='utf-8') as f:
        lines = [l for l in f if not l.startswith('#')]
    reader = csv.DictReader(lines, delimiter=';')
    return list(reader)


def _is_error(row):
    """Check if a CSV row indicates an error."""
    result = row.get('result', '')
    return any(s in result for s in ['Error', 'Forbidden', 'Not Found', 'INTERNAL', 'ConnectionError'])


def _is_warning(row):
    """Check if a CSV row indicates a real warning (not ignored, not a redirect)."""
    ws = row.get('warningstring', '')
    return bool(ws) and ws != 'ignored' and 'Redirected' not in ws


def count_status(rows):
    """Count total, errors, redirects, filtered, ignored, warnings."""
    total = len(rows)

    errors = sum(1 for r in rows if _is_error(r))
    redirects = sum(1 for r in rows if 'Redirected' in r.get('warningstring', ''))
    warnings = sum(1 for r in rows if _is_warning(r))
    ignored = sum(1 for r in rows if r.get('warningstring', '') == 'ignored')
    filtered = sum(1 for r in rows if r.get('result', '') == 'filtered')
    ok = total - errors - redirects - ignored - filtered

    return {
        'total': total, 'ok': ok, 'redirects': redirects,
        'filtered': filtered, 'ignored': ignored,
        'warnings': warnings, 'errors': errors,
    }


def extract_errors(rows):
    """Extract error URLs from CSV rows."""
    errors = []
    for r in rows:
        if _is_error(r):
            url = r.get('urlname', '')
            real = r.get('url', '')
            result = r.get('result', '')
            if url:
                if real and real != url:
                    errors.append(f'URL: {url}\n  Real URL: {real}\n  {result}')
                else:
                    errors.append(f'URL: {url}\n  {result}')
    return errors


def extract_warnings(rows):
    """Extract warning URLs from CSV rows (excluding redirects, which are shown separately)."""
    warnings = []
    for r in rows:
        if _is_warning(r):
            url = r.get('urlname', '')
            ws = r.get('warningstring', '')
            if url:
                warnings.append(f'URL: {url}\n  {ws}')
    return warnings


def extract_redirects(rows):
    """Return (original_url, final_url) pairs from CSV rows with redirects."""
    redirects = []
    for r in rows:
        if 'Redirected' in r.get('warningstring', ''):
            url = r.get('urlname', '')
            real = r.get('url', '')
            if url and real and url != real:
                redirects.append((url, real))
    return redirects


def load_silent_ignore(path):
    """Load silent-ignore patterns, return list of compiled regexes."""
    if not path or not os.path.isfile(path):
        return []
    patterns = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            patterns.append(re.compile(line))
    return patterns


def extract_ignored_urls(rows, silent_patterns):
    """Return ignored/filtered URLs, filtered by silent-ignore patterns."""
    urls = set()
    for r in rows:
        ws = r.get('warningstring', '')
        result = r.get('result', '')
        if ws == 'ignored' or result == 'filtered':
            url = r.get('url', '')
            if url:
                if not any(p.search(url) for p in silent_patterns):
                    urls.add(url)
    return sorted(urls)


def print_summary(text_output, csv_file, silent_ignore_path, out=print):
    """Print formatted summary to stdout. Returns the stats dict."""
    rows = parse_csv(csv_file)
    stats = count_status(rows)

    out('## Link Checker Results')
    out()
    out( '| Status                       | Count |')
    out( '|------------------------------|-------|')
    out(f'| 🔍 Total                     | {stats['total']:>5} |')
    out(f'| ✅ Successful                | {stats['ok']:>5} |')
    out(f'| 🔀 Redirected                | {stats['redirects']:>5} |')
    out(f'| 👻 Filtered (.linkcheckerrc) | {stats['filtered']:>5} |')
    out(f'| 👻 Ignored (e.g. mailto: )    | {stats['ignored']:>5} |')
    out(f'| ⚠️ Warnings                   | {stats['warnings']:>5} |')
    out(f'| ❌ Errors                     | {stats['errors']:>5} |')
    out()

    # Errors
    if stats['errors'] > 0:
        out('### Errors')
        out()
        for err in extract_errors(rows):
            out(err)
        out()

    # Warnings
    if stats['warnings'] > 0:
        out('### Warnings')
        out()
        for warn in extract_warnings(rows):
            out(warn)
        out()

    # Redirects
    redirects = extract_redirects(rows)
    if redirects:
        out('### Redirects')
        out()
        for url, real in redirects:
            out(f'- {url} --> {real}')
        out()

    # Filtered and ignored links
    out('### Filtered and ignored links (manual check recommended)')
    out()
    silent_patterns = load_silent_ignore(silent_ignore_path)
    for url in extract_ignored_urls(rows, silent_patterns):
        out(f'- {url}')
    out()

    # Stats: reconstruct summary from CSV, cross-check against text output
    text_total = None
    text_urls = None
    for line in text_output.splitlines():
        if "That's it" in line:
            line = strip_ansi(line)
            m = re.search(r'(\d+) links', line)
            if m:
                text_total = int(m.group(1))
            m = re.search(r'(\d+) URLs', line)
            if m:
                text_urls = int(m.group(1))
            break

    if text_total is None:
        out('Warning: could not find summary line in text output.')
        out(f"That's it. {stats['total']} links checked. {stats['warnings']} warnings, {stats['errors']} errors.")
    else:
        if text_total != stats['total']:
            out(f'Warning: CSV has {stats["total"]} links, text output has {text_total}.')
        if text_urls is None:
            out('Warning: could not extract URLs checked count from text output.')
            out(f"That's it. {stats['total']} links checked. {stats['warnings']} warnings, {stats['errors']} errors.")
        else:
            out(f"That's it. {stats['total']} links in {text_urls} URLs checked. {stats['warnings']} warnings, {stats['errors']} errors.")

    return stats


def main():
    parser = argparse.ArgumentParser(description='Run LinkChecker and produce a summary.')
    parser.add_argument('output', nargs='?', help='Write raw LinkChecker output to this file')
    parser.add_argument('--ignored', metavar='FILE', help='Write ignored URLs to this file')
    parser.add_argument('--ci', action='store_true', help='CI mode (use GITHUB_WORKSPACE)')
    args = parser.parse_args()

    # Determine paths
    if args.ci or os.environ.get('GITHUB_WORKSPACE'):
        base_dir = os.environ['GITHUB_WORKSPACE']
        public_dir = os.path.join(base_dir, 'public')
        config = os.path.join(base_dir, '.linkcheckerrc')
        silent_ignore = os.path.join(base_dir, 'linkchecker-silent-ignore')
    else:
        public_dir = os.path.join(SCRIPT_DIR, 'public')
        config = os.path.join(SCRIPT_DIR, '.linkcheckerrc')
        silent_ignore = os.path.join(SCRIPT_DIR, 'linkchecker-silent-ignore')

    if not os.path.isfile(config):
        print(f'Error: {config} not found.', file=sys.stderr)
        sys.exit(1)

    # Build site if needed (local only)
    if not args.ci and not os.path.isdir(public_dir):
        print('Building site...')
        subprocess.run(
            ['hugo', '--minify', '--baseURL', 'https://f4inx.github.io/'],
            cwd=SCRIPT_DIR, check=True,
        )

    # Prepare config and run
    with tempfile.TemporaryDirectory() as tmpdir:
        config_tmp = os.path.join(tmpdir, 'linkchecker.conf')
        csv_file = os.path.join(tmpdir, 'output.csv')
        prepare_config(config, public_dir, config_tmp)
        text_output = run_linkchecker(config_tmp, public_dir, csv_file)

        # Copy raw output if requested
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(text_output)
            print(f'Output written to {args.output}')

        # Print summary to stdout and, in CI, to GITHUB_STEP_SUMMARY
        step_summary = os.environ.get('GITHUB_STEP_SUMMARY')
        if args.ci and step_summary:
            # Summary with tee: stdout and file
            with open(step_summary, 'a', encoding='utf-8') as f:
                def out(s=''):
                    print(s, file=sys.stdout)
                    print(s, file=f)
                stats = print_summary(text_output, csv_file, silent_ignore, out=out)
        else:
            # Summary with just stdout
            stats = print_summary(text_output, csv_file, silent_ignore)

        # Extract ignored URLs if requested
        if args.ignored:
            rows = parse_csv(csv_file)
            silent_patterns = load_silent_ignore(silent_ignore)
            urls = extract_ignored_urls(rows, silent_patterns)
            with open(args.ignored, 'w') as f:
                for url in urls:
                    f.write(url + '\n')
            print(f'Ignored URLs written to {args.ignored}')
            print(f'Ignored: {len(urls)}')

    # Fail CI when errors or warnings were found
    if stats['errors'] > 0 or stats['warnings'] > 0:
        print(
            f"\nLink check failed: {stats['errors']} error(s), "
            f"{stats['warnings']} warning(s).",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == '__main__':
    main()
