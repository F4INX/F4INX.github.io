#!/usr/bin/env python3
"""Run LinkChecker and produce a formatted summary.

Usage:
    ./linkchecker.py [output.log] [--ignored ignored-urls.log]
    ./linkchecker.py --ci
"""

import argparse
import contextlib
import csv
import io
import os
import re
import subprocess
import sys
import tempfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

ANSI_RE = re.compile(r'\x1b\[[0-9;]*m')


def strip_ansi(text):
    return ANSI_RE.sub('', text)


def prepare_config(config_path, public_dir):
    """Replace PLACEHOLDER in config, return temp config path."""
    webroot = 'file://' + public_dir.replace(' ', '%20') + '/'
    with open(config_path) as f:
        content = f.read()
    content = content.replace('file:///PLACEHOLDER/', webroot)
    fd, tmp_path = tempfile.mkstemp(suffix='.conf')
    with os.fdopen(fd, 'w') as f:
        f.write(content)
    return tmp_path


@contextlib.contextmanager
def temp_config(config_path, public_dir):
    """Create a temporary config file, cleaned up on exit."""
    path = prepare_config(config_path, public_dir)
    try:
        yield path
    finally:
        os.unlink(path)


@contextlib.contextmanager
def temp_file(suffix):
    """Create a temporary file path, cleaned up on exit."""
    path = tempfile.mktemp(suffix=suffix)
    try:
        yield path
    finally:
        os.unlink(path)


def run_linkchecker(config, public_dir, csv_file):
    """Run LinkChecker, return captured stdout and write CSV file."""
    result = subprocess.run(
        [
            'linkchecker', '--config', config,
            '--check-extern', '--no-warnings', '-v', '--no-status',
            '-F', f'csv/utf-8/{csv_file}',
            public_dir + '/',
        ],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
    )
    return result.stdout


def parse_csv(csv_file):
    """Parse CSV, skip comment lines, return list of row dicts."""
    with open(csv_file, encoding='utf-8') as f:
        lines = [l for l in f if not l.startswith('#')]
    reader = csv.DictReader(lines, delimiter=';')
    return list(reader)


def _is_error(result):
    """Check if a CSV result field indicates an error."""
    return any(s in result for s in ['Error', 'Forbidden', 'Not Found', 'INTERNAL', 'ConnectionError'])


def count_status(rows, text_output):
    """Count total, errors, redirects, filtered, ignored, warnings."""
    total = 0
    for line in text_output.splitlines():
        line = strip_ansi(line)
        m = re.search(r'(\d+) links', line)
        if m:
            total = int(m.group(1))

    errors = sum(1 for r in rows if _is_error(r.get('result', '')))
    redirects = sum(1 for r in rows if 'Redirected' in r.get('warningstring', ''))
    warnings = sum(1 for r in rows if r.get('warningstring', '') and r.get('warningstring', '') != 'ignored' and 'Redirected' not in r.get('warningstring', ''))
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
        result = r.get('result', '')
        if _is_error(result):
            url = r.get('urlname', '')
            real = r.get('url', '')
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
        ws = r.get('warningstring', '')
        if ws and ws != 'ignored' and 'Redirected' not in ws:
            url = r.get('urlname', '')
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


def print_summary(text_output, csv_file, silent_ignore_path):
    """Print formatted summary to stdout. Returns the stats dict."""
    rows = parse_csv(csv_file)
    stats = count_status(rows, text_output)

    print('## Link Checker Results')
    print()
    print( '| Status                       | Count |')
    print( '|------------------------------|-------|')
    print(f'| 🔍 Total                     | {stats['total']:>5} |')
    print(f'| ✅ Successful                | {stats['ok']:>5} |')
    print(f'| 🔀 Redirected                | {stats['redirects']:>5} |')
    print(f'| 👻 Filtered (.linkcheckerrc) | {stats['filtered']:>5} |')
    print(f'| 👻 Ignored (e.g. mailto: )    | {stats['ignored']:>5} |')
    print(f'| ⚠️ Warnings                   | {stats['warnings']:>5} |')
    print(f'| ❌ Errors                     | {stats['errors']:>5} |')
    print()

    # Errors
    if stats['errors'] > 0:
        print('### Errors')
        print()
        for err in extract_errors(rows):
            print(err)
        print()

    # Warnings
    if stats['warnings'] > 0:
        print('### Warnings')
        print()
        for warn in extract_warnings(rows):
            print(warn)
        print()

    # Redirects
    redirects = extract_redirects(rows)
    if redirects:
        print('### Redirects')
        print()
        for url, real in redirects:
            print(f'- {url} --> {real}')
        print()

    # Filtered and ignored links
    print('### Filtered and ignored links (manual check recommended)')
    print()
    silent_patterns = load_silent_ignore(silent_ignore_path)
    for url in extract_ignored_urls(rows, silent_patterns):
        print(f'- {url}')
    print()

    # Stats
    for line in text_output.splitlines():
        if "That's it" in line:
            print(strip_ansi(line).strip())
            break

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
    with (
        temp_config(config, public_dir) as config_tmp,
        temp_file('.csv') as csv_file,
    ):
        text_output = run_linkchecker(config_tmp, public_dir, csv_file)

        # Copy raw output if requested
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(text_output)
            print(f'Output written to {args.output}')

        # Print summary to stdout and, in CI, to GITHUB_STEP_SUMMARY
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            stats = print_summary(text_output, csv_file, silent_ignore)
        summary = buf.getvalue()
        sys.stdout.write(summary)

        step_summary = os.environ.get('GITHUB_STEP_SUMMARY')
        if args.ci and step_summary:
            with open(step_summary, 'a', encoding='utf-8') as f:
                f.write(summary)

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
