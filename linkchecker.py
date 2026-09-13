#!/usr/bin/env python3
"""Run LinkChecker via its Python API and produce a formatted summary.

Usage:
    ./linkchecker.py [--ignored ignored-urls.log]
    ./linkchecker.py --ci
    ./linkchecker.py --local-server [--port PORT]
    ./linkchecker.py --no-cache

By default the script auto-detects a running Hugo dev server on
localhost:1313 and checks links against it. If no server is found, it
falls back to checking files in public/. Use --local-server to require
the dev server and exit with an error if it is not running.

External links that were successfully checked are cached in
.linkchecker-cache.json (TTL 24h by default, configurable with
--cache-ttl). Use --no-cache to bypass the cache and check all links.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request
from datetime import datetime, timedelta
from urllib.parse import urlparse

from linkcheck import configuration
from linkcheck.cmdline import aggregate_url
from linkcheck.director import check_urls, get_aggregate
from linkcheck.logger import _Logger

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

DEFAULT_SERVER_PORT = 1313
CACHE_FILE = '.linkchecker-cache.json'
DEFAULT_CACHE_TTL_HOURS = 24
CACHE_MAX_AGE_DAYS = 30
IGNORE_FILE = 'linkchecker-ignore'
USER_AGENT = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
              '(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36')


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


def load_ignore_patterns(path):
    """Load regex patterns from a file, return a list of externlinks entries.

    Each line is a regex pattern. Blank lines and lines starting with # are
    skipped. Each entry is a dict matching LinkChecker's externlinks format:
    {'pattern': compiled_regex, 'negate': False, 'strict': 1}
    """
    if not path or not os.path.isfile(path):
        return []
    entries = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            try:
                entries.append({
                    'pattern': re.compile(line),
                    'negate': False,
                    'strict': 1,
                })
            except re.error as e:
                print(f'Warning: invalid regex in {path}: {line!r}: {e}',
                      file=sys.stderr)
    return entries


def run_linkchecker(public_dir, ignore_entries, entry_url=None, base_url=None):
    """Run LinkChecker via its Python API, return list of url_data objects.

    Uses a custom CollectorLogger that collects url_data objects directly,
    eliminating the need for CSV files and text output parsing.

    entry_url is the URL to start crawling from. In file mode this is a
    file:// path; in server mode it is an http://localhost:PORT/ URL.
    """
    config = configuration.Configuration()
    config.sanitize()

    config.logger_add(CollectorLogger)
    config['logger'] = config.logger_new('collector')
    config['checkextern'] = True
    config['verbose'] = True
    config['warnings'] = False
    config['status'] = False
    config['useragent'] = USER_AGENT
    config['externlinks'] = ignore_entries
    if not base_url:
        config['localwebroot'] = 'file://' + public_dir.replace(' ', '%20') + '/'

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


def count_status(rows, cached_urls=None):
    """Count total, errors, redirects, filtered, ignored, warnings, cached.

    Cached URLs appear as 'filtered' in the results (they were added to the
    ignore list). The cached_urls set lets us separate them from links
    filtered by the ignore patterns file.
    """
    total = len(rows)

    errors = sum(1 for r in rows if _is_error(r))
    redirects = sum(1 for r in rows
                    if any('Redirected' in w[1] for w in r.warnings))
    warnings = sum(1 for r in rows if _is_warning(r))
    ignored = sum(1 for r in rows if _is_ignored(r))

    cached_urls = cached_urls or set()
    cached = 0
    filtered = 0
    for r in rows:
        if r.result == 'filtered':
            if r.url in cached_urls or r.base_url in cached_urls:
                cached += 1
            else:
                filtered += 1

    ok = total - errors - redirects - ignored - filtered - cached

    return {
        'total': total, 'ok': ok, 'redirects': redirects,
        'filtered': filtered, 'ignored': ignored,
        'warnings': warnings, 'errors': errors, 'cached': cached,
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


def extract_ignored_urls(rows, silent_patterns, cached_urls=None):
    """Return ignored/filtered URLs, filtered by silent-ignore patterns.

    Cached URLs (skipped via the cache) are excluded — they are not
    manually ignored and don't need checking.
    """
    cached_urls = cached_urls or set()
    urls = set()
    for r in rows:
        if _is_ignored(r) or r.result == 'filtered':
            url = r.url
            if url and url not in cached_urls and r.base_url not in cached_urls:
                if not any(p.search(url) for p in silent_patterns):
                    urls.add(url)
    return sorted(urls)


def is_external_url(url):
    """Check if a URL is an external link (http/https, not localhost)."""
    if not url:
        return False
    parsed = urlparse(url)
    if parsed.scheme not in ('http', 'https'):
        return False
    if parsed.hostname in ('localhost', '127.0.0.1', '::1'):
        return False
    return True


def load_cache(path):
    """Load the external-link cache. Returns a dict (URL -> entry) or empty dict."""
    if not path or not os.path.isfile(path):
        return {}
    try:
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return {}
        return data
    except (json.JSONDecodeError, OSError) as e:
        print(f'Warning: could not read cache {path}: {e}', file=sys.stderr)
        return {}


def save_cache(path, cache):
    """Write the cache to disk as JSON."""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(cache, f, indent=2, sort_keys=True)
    except OSError as e:
        print(f'Warning: could not write cache {path}: {e}', file=sys.stderr)


def get_fresh_cached_urls(cache, ttl_hours):
    """Return the set of URLs whose cache entry is still within the TTL.

    Only OK results are stored in the cache, so every fresh entry is a link
    that was reachable last time and can be skipped.
    """
    cutoff = datetime.now() - timedelta(hours=ttl_hours)
    fresh = set()
    for url, entry in cache.items():
        try:
            cached_at = datetime.fromisoformat(entry['cached_at'])
        except (KeyError, ValueError, TypeError):
            continue
        if cached_at > cutoff:
            fresh.add(url)
    return fresh


def update_cache(cache, rows, now):
    """Update cache with results for external URLs that were actually checked.

    Uses base_url (the URL as it appears in the HTML) as the cache key,
    so that redirecting links are cached by their original URL — the one
    LinkChecker will encounter on the next run.

    Only OK results are stored; error/warning entries are removed so they
    will be rechecked on the next run.
    """
    for ud in rows:
        url = ud.base_url
        if not url or not is_external_url(url):
            continue
        if ud.result in ('filtered', 'ignored'):
            continue
        if _is_error(ud) or _is_warning(ud):
            cache.pop(url, None)
        else:
            cache[url] = {
                'result': ud.result,
                'cached_at': now.isoformat(),
            }
    return cache


def prune_cache(cache, max_age_days=CACHE_MAX_AGE_DAYS):
    """Remove entries older than max_age_days to prevent unbounded growth."""
    cutoff = datetime.now() - timedelta(days=max_age_days)
    pruned = {}
    for url, entry in cache.items():
        try:
            cached_at = datetime.fromisoformat(entry['cached_at'])
        except (KeyError, ValueError, TypeError):
            continue
        if cached_at > cutoff:
            pruned[url] = entry
    return pruned


def build_cache_entries(urls):
    """Build externlinks entries for cached URLs (exact match)."""
    return [
        {'pattern': re.compile(f'^{re.escape(url)}$'), 'negate': False, 'strict': 1}
        for url in sorted(urls)
    ]


def print_summary(rows, silent_ignore_path, out=print, cached_urls=None):
    """Print formatted summary to stdout. Returns the stats dict."""
    stats = count_status(rows, cached_urls=cached_urls)

    out('## Link Checker Results')
    out()
    out( '| Status                       | Count |')
    out( '|------------------------------|-------|')
    out(f'| 🔍 Total                     | {stats['total']:>5} |')
    out(f'| ✅ Successful                | {stats['ok']:>5} |')
    out(f'| 🔀 Redirected                | {stats['redirects']:>5} |')
    out(f'| 👻 Filtered (ignore list)    | {stats['filtered']:>5} |')
    out(f'| 👻 Ignored (e.g. mailto: )    | {stats['ignored']:>5} |')
    if stats['cached'] > 0:
        out(f'| 💾 Cached (skipped)          | {stats['cached']:>5} |')
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
    for url in extract_ignored_urls(rows, silent_patterns,
                                     cached_urls=cached_urls):
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
    parser.add_argument('--cache-ttl', type=float, default=DEFAULT_CACHE_TTL_HOURS,
                        metavar='HOURS',
                        help=f'TTL for cached external links in hours '
                             f'(default: {DEFAULT_CACHE_TTL_HOURS})')
    parser.add_argument('--no-cache', action='store_true',
                        help='Disable external link cache (always check all links)')
    args = parser.parse_args()

    # Determine paths
    if args.ci or os.environ.get('GITHUB_WORKSPACE'):
        base_dir = os.environ['GITHUB_WORKSPACE']
        public_dir = os.path.join(base_dir, 'public')
        ignore_file = os.path.join(base_dir, IGNORE_FILE)
        silent_ignore = os.path.join(base_dir, 'linkchecker-silent-ignore')
    else:
        base_dir = SCRIPT_DIR
        public_dir = os.path.join(SCRIPT_DIR, 'public')
        ignore_file = os.path.join(SCRIPT_DIR, IGNORE_FILE)
        silent_ignore = os.path.join(SCRIPT_DIR, 'linkchecker-silent-ignore')

    if not os.path.isfile(ignore_file):
        print(f'Error: {ignore_file} not found.', file=sys.stderr)
        sys.exit(1)

    # Load ignore patterns and combine with cached URL entries
    ignore_entries = load_ignore_patterns(ignore_file)
    use_cache = not args.no_cache
    if use_cache:
        cache_path = os.path.join(base_dir, CACHE_FILE)
        cache = load_cache(cache_path)
        fresh_cached = get_fresh_cached_urls(cache, args.cache_ttl)
        if fresh_cached:
            print(f'Cache: {len(fresh_cached)} external links skipped '
                  f'(TTL {args.cache_ttl}h)')
        ignore_entries += build_cache_entries(fresh_cached)
    else:
        cache_path = None
        cache = {}
        fresh_cached = set()

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
    rows = run_linkchecker(public_dir, ignore_entries,
                           entry_url=entry_url, base_url=server_url)

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
            stats = print_summary(rows, silent_ignore, out=out,
                                  cached_urls=fresh_cached)
    else:
        stats = print_summary(rows, silent_ignore, cached_urls=fresh_cached)

    # Extract ignored URLs if requested
    if args.ignored:
        silent_patterns = load_silent_ignore(silent_ignore)
        urls = extract_ignored_urls(rows, silent_patterns,
                                    cached_urls=fresh_cached)
        with open(args.ignored, 'w') as f:
            for url in urls:
                f.write(url + '\n')
        print(f'Ignored URLs written to {args.ignored}')
        print(f'Ignored: {len(urls)}')

    # Update and save the cache with freshly checked external links
    if use_cache:
        now = datetime.now()
        update_cache(cache, rows, now)
        cache = prune_cache(cache)
        save_cache(cache_path, cache)
        checked = len(rows) - stats['cached']
        print(f'Cache: {len(cache)} entries saved to {cache_path} '
              f'({checked} links checked this run)')

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
