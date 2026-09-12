#!/usr/bin/env python3
"""Run LinkChecker via its Python API and produce a formatted summary.

Usage:
    ./linkchecker.py [--ignored ignored-urls.log]
    ./linkchecker.py --ci
    ./linkchecker.py --local-server [--port PORT]

By default the script auto-detects a running Hugo dev server on
localhost:1313 and checks links against it. If no server is found, it
falls back to checking files in public/. Use --local-server to require
the dev server and exit with an error if it is not running.
"""

import argparse
import os
import re
import subprocess
import sys
import tempfile
import urllib.request

from linkcheck import configuration
from linkcheck.cmdline import aggregate_url
from linkcheck.director import check_urls, get_aggregate
from linkcheck.logger import _Logger

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

DEFAULT_SERVER_PORT = 1313


class CollectorLogger(_Logger):
    """Collect url_data objects in a list instead of writing to a file."""

    LoggerName = "collector"
    LoggerArgs = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows = []

    def start_output(self):
        super().start_output()

    def log_url(self, url_data):
        self.rows.append(url_data)

    def end_output(self, **kwargs):
        pass


def probe_server(port=DEFAULT_SERVER_PORT, timeout=2):
    """Check whether a Hugo dev server is reachable on localhost.

    Returns the server URL (e.g. 'http://localhost:1313/') if reachable,
    None otherwise.
    """
    url = f'http://localhost:{port}/'
    try:
        req = urllib.request.Request(url, method='HEAD')
        urllib.request.urlopen(req, timeout=timeout)
        return url
    except Exception:
        return None


def prepare_config(config_path, public_dir, output_path, base_url=None):
    """Replace PLACEHOLDER in config and write the result to output_path.

    When base_url is given (server mode), use it as the localwebroot instead
    of a file:// path. This lets LinkChecker crawl a running dev server.
    """
    if base_url:
        webroot = base_url
    else:
        webroot = 'file://' + public_dir.replace(' ', '%20') + '/'
    with open(config_path) as f:
        content = f.read()
    content = content.replace('file:///PLACEHOLDER/', webroot)
    with open(output_path, 'w') as f:
        f.write(content)


def run_linkchecker(config_path, public_dir, entry_url=None, base_url=None):
    """Run LinkChecker via its Python API, return list of url_data objects.

    Uses a custom CollectorLogger that collects url_data objects directly,
    eliminating the need for CSV files and text output parsing.

    entry_url is the URL to start crawling from. In file mode this is a
    file:// path; in server mode it is an http://localhost:PORT/ URL.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        config_tmp = os.path.join(tmpdir, 'linkchecker.conf')
        prepare_config(config_path, public_dir, config_tmp, base_url=base_url)

        config = configuration.Configuration()
        config.read(files=[config_tmp])
        config.sanitize()

        config.logger_add(CollectorLogger)
        config['logger'] = config.logger_new('collector')
        config['verbose'] = True
        config['warnings'] = False
        config['status'] = False

        aggregate = get_aggregate(config)
        aggregate_url(aggregate, entry_url or (public_dir + '/'))
        check_urls(aggregate)

        return config['logger'].rows


def _is_error(ud):
    """Check if a url_data object indicates an error."""
    return not ud.valid and ud.result != 'filtered'


def _is_warning(ud):
    """Check if a url_data object has a real warning (not a redirect)."""
    return bool(ud.warnings) and all(
        'Redirected' not in w[1] for w in ud.warnings
    )


def _is_ignored(ud):
    """Check if a url_data object was ignored (mailto, tel, etc.)."""
    return any(w[0] == 'ignored' for w in ud.warnings) if ud.warnings else False


def count_status(rows):
    """Count total, errors, redirects, filtered, ignored, warnings."""
    total = len(rows)

    errors = sum(1 for r in rows if _is_error(r))
    redirects = sum(1 for r in rows
                    if any('Redirected' in w[1] for w in r.warnings))
    warnings = sum(1 for r in rows if _is_warning(r))
    ignored = sum(1 for r in rows if _is_ignored(r))
    filtered = sum(1 for r in rows if r.result == 'filtered')
    ok = total - errors - redirects - ignored - filtered

    return {
        'total': total, 'ok': ok, 'redirects': redirects,
        'filtered': filtered, 'ignored': ignored,
        'warnings': warnings, 'errors': errors,
    }


def extract_errors(rows):
    """Extract error URLs from url_data objects."""
    errors = []
    for r in rows:
        if _is_error(r):
            url = r.base_url
            real = r.url
            result = r.result
            if real and real != url:
                errors.append(f'URL: {url}\n  Real URL: {real}\n  {result}')
            else:
                errors.append(f'URL: {url}\n  {result}')
    return errors


def extract_warnings(rows):
    """Extract warning URLs from url_data objects (excluding redirects)."""
    warnings = []
    for r in rows:
        if _is_warning(r):
            url = r.base_url
            ws = '\n'.join(w[1] for w in r.warnings)
            if url:
                warnings.append(f'URL: {url}\n  {ws}')
    return warnings


def extract_redirects(rows):
    """Return (original_url, final_url) pairs from url_data objects with redirects."""
    redirects = []
    for r in rows:
        if any('Redirected' in w[1] for w in r.warnings):
            url = r.base_url
            real = r.url
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
            try:
                patterns.append(re.compile(line))
            except re.error as e:
                print(f'Warning: invalid regex in {path}: {line!r}: {e}', file=sys.stderr)
    return patterns


def extract_ignored_urls(rows, silent_patterns):
    """Return ignored/filtered URLs, filtered by silent-ignore patterns."""
    urls = set()
    for r in rows:
        if _is_ignored(r) or r.result == 'filtered':
            url = r.url
            if url:
                if not any(p.search(url) for p in silent_patterns):
                    urls.add(url)
    return sorted(urls)


def print_summary(rows, silent_ignore_path, out=print):
    """Print formatted summary to stdout. Returns the stats dict."""
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

    out(f"That's it. {stats['total']} links checked. {stats['warnings']} warnings, {stats['errors']} errors.")

    return stats


def main():
    parser = argparse.ArgumentParser(description='Run LinkChecker and produce a summary.')
    parser.add_argument('--ignored', metavar='FILE', help='Write ignored URLs to this file')
    parser.add_argument('--ci', action='store_true', help='CI mode (use GITHUB_WORKSPACE)')
    parser.add_argument('--local-server', action='store_true',
                        help='Check the local dev server instead of files in public/')
    parser.add_argument('--port', type=int, default=DEFAULT_SERVER_PORT,
                        help=f'Port for the local dev server (default: {DEFAULT_SERVER_PORT})')
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

    # Determine whether to use server mode or file mode.
    # Server mode is never used in CI.
    server_url = None
    if not args.ci:
        if args.local_server:
            server_url = probe_server(port=args.port)
            if not server_url:
                print(f'Error: no dev server found on localhost:{args.port}.',
                      file=sys.stderr)
                print('Start one with: hugo server', file=sys.stderr)
                sys.exit(1)
        else:
            # Auto-detect: probe the dev server, fall back to file mode.
            server_url = probe_server(port=args.port)
            if server_url:
                print(f'Dev server detected at {server_url}')
            else:
                print('No dev server detected, checking local files instead.')
                print('Start one with: hugo server')

    if server_url:
        print(f'Checking links on {server_url}')
    else:
        # File mode: build site if needed (local only)
        if not args.ci and not os.path.isdir(public_dir):
            print('Building site...')
            subprocess.run(
                ['hugo', '--minify', '--baseURL', 'https://f4inx.github.io/'],
                cwd=SCRIPT_DIR, check=True,
            )

    # Run LinkChecker via Python API
    if server_url:
        entry_url = server_url
    else:
        entry_url = public_dir + '/'
    rows = run_linkchecker(config, public_dir, entry_url=entry_url,
                           base_url=server_url)

    if not rows:
        print('Error: LinkChecker did not produce any results.', file=sys.stderr)
        sys.exit(1)

    # Print summary to stdout and, in CI, to GITHUB_STEP_SUMMARY
    step_summary = os.environ.get('GITHUB_STEP_SUMMARY')
    if args.ci and step_summary:
        with open(step_summary, 'a', encoding='utf-8') as f:
            # Tees to stdout and the step summary file. Captures f from the
            # enclosing with block, so out is only valid while it is open —
            # print_summary must call it synchronously, not store it.
            def out(s=''):
                print(s, file=sys.stdout)
                print(s, file=f)
            stats = print_summary(rows, silent_ignore, out=out)
    else:
        stats = print_summary(rows, silent_ignore)

    # Extract ignored URLs if requested
    if args.ignored:
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
