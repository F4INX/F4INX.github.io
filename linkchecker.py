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


def run_linkchecker(config, public_dir, text_log, csv_file):
    """Run LinkChecker, write text log and CSV file."""
    with open(text_log, 'w') as log:
        subprocess.run(
            [
                'linkchecker', '--config', config,
                '--check-extern', '--no-warnings', '-v', '--no-status',
                '-F', f'csv/utf-8/{csv_file}',
                public_dir + '/',
            ],
            stdout=log, stderr=subprocess.STDOUT,
        )


def parse_csv(csv_file):
    """Parse CSV, skip comment lines, return list of row dicts."""
    with open(csv_file, encoding='utf-8') as f:
        lines = [l for l in f if not l.startswith('#')]
    reader = csv.DictReader(lines, delimiter=';')
    return list(reader)


def count_status(rows, text_log):
    """Count total, errors, redirects, filtered, ignored, warnings."""
    total = 0
    warnings = 0
    for line in open(text_log, encoding='utf-8', errors='replace'):
        line = strip_ansi(line)
        m = re.search(r'(\d+) links', line)
        if m:
            total = int(m.group(1))
        m = re.search(r'(\d+) warnings', line)
        if m:
            warnings = int(m.group(1))

    errors = sum(1 for r in rows if 'Error' in r.get('result', ''))
    redirects = sum(1 for r in rows if 'Redirected' in r.get('warningstring', ''))
    ignored = sum(1 for r in rows if r.get('warningstring', '') == 'ignored')
    filtered = sum(1 for r in rows if r.get('result', '') == 'filtered')
    ok = total - errors - redirects - ignored - filtered

    return {
        'total': total, 'ok': ok, 'redirects': redirects,
        'filtered': filtered, 'ignored': ignored,
        'warnings': warnings, 'errors': errors,
    }


def extract_errors(text_log):
    """Extract error lines from text log (for Real URL context)."""
    lines = strip_ansi(open(text_log, encoding='utf-8', errors='replace').read()).splitlines()
    errors = []
    for i, line in enumerate(lines):
        if 'Result     Error' in line:
            # Look backwards for Real URL
            for j in range(i, max(i - 10, -1), -1):
                if lines[j].startswith('Real URL   '):
                    url = lines[j].replace('Real URL   ', 'URL: ', 1)
                    result = line.replace('Result     ', '  ', 1)
                    errors.append(f'{url}\n{result}')
                    break
    return errors


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
    for line in open(path, encoding='utf-8'):
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


def print_summary(text_log, csv_file, silent_ignore_path):
    """Print formatted summary to stdout."""
    rows = parse_csv(csv_file)
    stats = count_status(rows, text_log)

    print('## Link Checker Results')
    print()
    print( '| Status                    | Count |')
    print( '|---------------------------|-------|')
    print(f'| Total                     | {stats['total']:>5} |')
    print(f'| OK                        | {stats['ok']:>5} |')
    print(f'| Redirects                 | {stats['redirects']:>5} |')
    print(f'| Filtered (.linkcheckerrc) | {stats['filtered']:>5} |')
    print(f'| Ignored (e.g. mailto: )   | {stats['ignored']:>5} |')
    print(f'| Warnings                  | {stats['warnings']:>5} |')
    print(f'| Errors                    | {stats['errors']:>5} |')
    print()

    # Errors
    if stats['errors'] > 0:
        print('### Errors')
        print()
        for err in extract_errors(text_log):
            print(err)
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
    for line in open(text_log, encoding='utf-8', errors='replace'):
        if "That's it" in line:
            print(strip_ansi(line).strip())
            break


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
    config_tmp = prepare_config(config, public_dir)
    text_log = tempfile.mktemp(suffix='.log')
    csv_file = tempfile.mktemp(suffix='.csv')
    run_linkchecker(config_tmp, public_dir, text_log, csv_file)

    # Copy raw output if requested
    if args.output:
        import shutil
        shutil.copy(text_log, args.output)
        print(f'Output written to {args.output}')

    # Print summary
    print_summary(text_log, csv_file, silent_ignore)

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

    # Cleanup
    os.unlink(config_tmp)
    os.unlink(text_log)
    os.unlink(csv_file)


if __name__ == '__main__':
    main()
