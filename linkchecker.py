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
import time
import urllib.request
from datetime import datetime, timedelta
from urllib.parse import unquote, urlparse

import yaml

from linkcheck import configuration
from linkcheck.cmdline import aggregate_url
from linkcheck.director import check_urls, get_aggregate
from linkcheck.logger import _Logger

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

DEFAULT_SERVER_PORT = 1313
CACHE_FILE = '.linkchecker-cache.json'
DEFAULT_CACHE_TTL_HOURS = 24
CACHE_MAX_AGE_DAYS = 30
CLOUDFLARE_CACHE_TTL_HOURS = 30 * 24
DEFAULT_RECHECK_RATE = 2.0
CONFIG_FILE = 'linkchecker-config.yaml'
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


def fetch_public_ip(timeout=5):
    """Fetch the runner's public IPv4 and IPv6 addresses.

    Returns a string suitable for display in the summary, or None if
    the lookups fail.
    """
    ipv4 = None
    ipv6 = None
    try:
        ipv4 = urllib.request.urlopen(
            'https://api.ipify.org', timeout=timeout).read().decode().strip()
    except Exception:
        pass
    try:
        ipv6 = urllib.request.urlopen(
            'https://api6.ipify.org', timeout=timeout).read().decode().strip()
    except Exception:
        pass
    parts = []
    parts.append(f'IPv4: {ipv4 or "none"}')
    parts.append(f'IPv6: {ipv6 or "none"}')
    return ' | '.join(parts)


def load_config(path):
    """Load link checker configuration from a YAML file.

    Returns a dict with keys 'ignore', 'recheck', 'silent', each a list
    of compiled regex patterns.
    """
    result = {'ignore': [], 'recheck': [], 'silent': []}
    if not path or not os.path.isfile(path):
        return result
    with open(path, encoding='utf-8') as f:
        data = yaml.safe_load(f) or {}
    for section in ('ignore', 'recheck', 'silent'):
        patterns = data.get(section, []) or []
        for line in patterns:
            try:
                result[section].append(re.compile(line))
            except re.error as e:
                print(f'Warning: invalid regex in {path} [{section}]: '
                      f'{line!r}: {e}', file=sys.stderr)
    return result


def _externlinks_from_patterns(patterns):
    """Convert compiled regex patterns to LinkChecker externlinks entries."""
    return [
        {'pattern': p, 'negate': False, 'strict': 1}
        for p in patterns
    ]


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
    config['maxrequestspersecond'] = 5
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


def count_status(rows, cached_urls=None, cache=None, recovered=None):
    """Count total, errors, redirects, filtered, ignored, warnings, cached.

    Cached URLs appear as 'filtered' in the results (they were added to the
    ignore list). The cached_urls set lets us separate them from links
    filtered by the ignore patterns file. Cached URLs that have a
    final_url in the cache are counted separately as cached redirects.
    URLs in the `recovered` set (error URLs cleared by the primp
    recheck) are not counted as errors.
    """
    recovered = recovered or set()
    total = len(rows)

    errors = sum(1 for r in rows
                 if _is_error(r) and r.base_url not in recovered)
    redirects = sum(1 for r in rows
                    if any('Redirected' in w[1] for w in r.warnings))
    warnings = sum(1 for r in rows if _is_warning(r))
    ignored = sum(1 for r in rows if _is_ignored(r))

    cached_urls = cached_urls or set()
    cached = 0
    cached_redirects = 0
    filtered = 0
    for r in rows:
        if r.result == 'filtered':
            if r.url in cached_urls or r.base_url in cached_urls:
                cached += 1
                if cache:
                    key = r.base_url if r.base_url in cache else r.url
                    if key in cache and 'final_url' in cache[key]:
                        cached_redirects += 1
            else:
                filtered += 1

    ok = total - errors - redirects - ignored - filtered - cached

    return {
        'total': total, 'ok': ok, 'redirects': redirects,
        'filtered': filtered, 'ignored': ignored,
        'warnings': warnings, 'errors': errors, 'cached': cached,
        'cached_redirects': cached_redirects,
    }


def extract_errors(rows, recovered=None):
    """Extract error URLs from url_data objects.

    URLs in the `recovered` set (error URLs cleared by the primp
    recheck, see print_summary) are excluded.
    """
    recovered = recovered or set()
    errors = []
    for r in rows:
        if _is_error(r) and r.base_url not in recovered:
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


def normalize_url(url):
    """Normalize a URL for comparison by percent-decoding it.

    LinkChecker sometimes percent-encodes characters like ':' in paths,
    causing false-positive redirects (e.g. File: vs File%3A). Decoding
    both sides before comparing eliminates these.
    """
    return unquote(url)


def renormalize_cache(cache):
    """Fix existing cache entries affected by false-positive redirects.

    Removes 'final_url' from entries where the normalized base URL and
    final URL are identical (i.e., the only difference was percent-encoding).
    This is a one-time migration step for caches written before the
    normalization fix.
    """
    for url, entry in cache.items():
        final = entry.get('final_url')
        if final and normalize_url(url) == normalize_url(final):
            del entry['final_url']
    return cache


def extract_redirects(rows):
    """Return (original_url, final_url) pairs from url_data objects with redirects.

    Redirects where the normalized URLs are identical (i.e., the only
    difference is percent-encoding) are skipped as false positives.
    """
    redirects = []
    for r in rows:
        if any('Redirected' in w[1] for w in r.warnings):
            url = r.base_url
            real = r.url
            if url and real and url != real:
                if normalize_url(url) == normalize_url(real):
                    continue
                redirects.append((url, real))
    return redirects


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
    that was reachable last time and can be skipped. Cloudflare-blocked
    entries carry their own longer ttl_hours so they are skipped for a
    month instead of the default TTL.
    """
    now = datetime.now()
    fresh = set()
    for url, entry in cache.items():
        try:
            cached_at = datetime.fromisoformat(entry['cached_at'])
        except (KeyError, ValueError, TypeError):
            continue
        entry_ttl = entry.get('ttl_hours', ttl_hours)
        cutoff = now - timedelta(hours=entry_ttl)
        if cached_at > cutoff:
            fresh.add(url)
    return fresh


def update_cache(cache, rows, now):
    """Update cache with results for external URLs that were actually checked.

    Uses base_url (the URL as it appears in the HTML) as the cache key,
    so that redirecting links are cached by their original URL — the one
    LinkChecker will encounter on the next run.

    Only OK results are stored; error/warning entries are removed so they
    will be rechecked on the next run. When a URL was redirected, the
    final URL is stored as 'final_url' so the redirect can be displayed
    even on cached runs.
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
            entry = {
                'result': ud.result,
                'cached_at': now.isoformat(),
            }
            real = ud.url
            if real and real != url and normalize_url(url) != normalize_url(real):
                entry['final_url'] = real
            cache[url] = entry
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


def _is_cloudflare_block(status, headers):
    """Detect a Cloudflare bot-protection block from response headers.

    Returns True when the response carries a cf-mitigated header, or when
    the server is Cloudflare and the status is 403/503.
    """
    if 'cf-mitigated' in headers:
        return True
    server = headers.get('server', '').lower()
    if server == 'cloudflare' and status in (403, 503):
        return True
    return False


def recheck_urls(urls, rate=DEFAULT_RECHECK_RATE):
    """Recheck URLs using primp with browser impersonation.

    Requests are paced at `rate` per second to avoid tripping bot
    protection. Returns (lines, results) where lines is a list of strings
    for the summary, and results is a list of (url, status_code, ok,
    cloudflare) tuples. ok is True for 2xx/3xx status codes. cloudflare is
    True when the response was identified as a Cloudflare bot-protection
    block.
    """
    lines = []

    try:
        import primp
    except ImportError:
        lines.append('### Rechecked links (primp)')
        lines.append('')
        lines.append('primp not available — skipped.')
        lines.append('')
        return lines, []

    results = []
    ok_count = 0
    fail_count = 0
    cloudflare_count = 0

    client = primp.Client(impersonate="chrome", follow_redirects=True)
    delay = 1.0 / rate if rate > 0 else 0.0

    for i, url in enumerate(sorted(urls)):
        if i and delay:
            time.sleep(delay)
        try:
            response = client.get(url, timeout=30)
            status = response.status_code
            headers = dict(response.headers)
            cloudflare = _is_cloudflare_block(status, headers)
            ok = 200 <= status < 400
            results.append((url, status, ok, cloudflare))
            if cloudflare:
                cloudflare_count += 1
            elif ok:
                ok_count += 1
            else:
                fail_count += 1
        except Exception:
            results.append((url, None, False, False))
            fail_count += 1

    lines.append('### Rechecked links (primp, browser impersonation)')
    lines.append('')
    lines.append('| Status | Count |')
    lines.append('|--------|-------|')
    lines.append(f'| ✅ OK   | {ok_count:>5} |')
    lines.append(f'| ❌ Fail | {fail_count:>5} |')
    if cloudflare_count:
        lines.append(f'| 🛡️ Cloudflare | {cloudflare_count:>5} |')
    lines.append('')

    for url, status, ok, cloudflare in results:
        if cloudflare:
            lines.append(f'- 🛡️ {status} {url}')
        elif ok:
            lines.append(f'- ✅ {status} {url}')
        elif status is not None:
            lines.append(f'- ❌ {status} {url}')
        else:
            lines.append(f'- ❌ (exception) {url}')

    lines.append('')
    return lines, results


def print_summary(rows, silent_patterns, out=print, cached_urls=None,
                  public_ip=None, recheck_results=None, cache=None):
    """Print formatted summary to stdout. Returns the stats dict."""
    # Error URLs cleared by the primp recheck: either the target
    # responds to a browser-like client (link works, not an error), or
    # it is a Cloudflare block, which is cached and reported separately.
    recovered = set()
    if recheck_results:
        for url, status, ok, cloudflare in recheck_results:
            if ok or cloudflare:
                recovered.add(url)
    stats = count_status(rows, cached_urls=cached_urls, cache=cache,
                         recovered=recovered)

    # Compute recheck stats
    recheck_ok = 0
    recheck_fail = 0
    recheck_cloudflare = 0
    if recheck_results:
        for url, status, ok, cloudflare in recheck_results:
            if cloudflare:
                recheck_cloudflare += 1
            elif ok:
                recheck_ok += 1
            else:
                recheck_fail += 1

    # Cached Cloudflare-blocked URLs (from cache, not rechecked this run)
    cached_cloudflare = []
    if cache and cached_urls:
        for url, entry in cache.items():
            if url in cached_urls and entry.get('cloudflare'):
                cached_cloudflare.append(
                    (url, int(entry.get('result', 0))))
    cached_cloudflare.sort()

    # Build set of rechecked URLs to exclude from filtered list
    recheck_urls_set = set()
    if recheck_results:
        for url, status, ok, cloudflare in recheck_results:
            recheck_urls_set.add(url)

    if public_ip:
        out(f'**Runner IP:** {public_ip}')
        out()

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
        if stats['cached_redirects'] > 0:
            out(f'|  └─ 🔀 Cached redirects       | {stats['cached_redirects']:>5} |')
    out(f'| ⚠️ Warnings                   | {stats['warnings']:>5} |')
    out(f'| ❌ Errors                     | {stats['errors']:>5} |')
    if recheck_results:
        out(f'| 🔄 Rechecked (primp)         | {recheck_ok:>5} |')
        out(f'| ❌ Recheck errors             | {recheck_fail:>5} |')
        if recheck_cloudflare:
            out(f'| 🛡️ Cloudflare blocked        | {recheck_cloudflare:>5} |')
    if cached_cloudflare:
        out(f'| 🛡️ Cloudflare (cached)       | {len(cached_cloudflare):>5} |')
    out()

    # Errors
    if stats['errors'] > 0:
        out('### Errors')
        out()
        for err in extract_errors(rows, recovered):
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

    # Cached redirects (from cache entries with a final_url)
    cached_redirects = []
    if cache and cached_urls:
        for url, entry in cache.items():
            if url in cached_urls and 'final_url' in entry:
                cached_redirects.append((url, entry['final_url']))
    if cached_redirects:
        cached_redirects.sort()
        out('### Cached redirects (from cache)')
        out()
        for url, real in cached_redirects:
            out(f'- {url} --> {real}')
        out()

    # Filtered and ignored links (exclude rechecked URLs)
    out('### Filtered and ignored links (manual check recommended)')
    out()
    for url in extract_ignored_urls(rows, silent_patterns,
                                     cached_urls=cached_urls):
        if url not in recheck_urls_set:
            out(f'- {url}')
    out()

    # Rechecked links detail (primp)
    if recheck_results:
        # Non-Cloudflare results
        non_cf = [(url, status, ok) for url, status, ok, cf in recheck_results
                  if not cf]
        if non_cf:
            out('### Rechecked links (primp, browser impersonation)')
            out()
            for url, status, ok in non_cf:
                if ok:
                    out(f'- ✅ {status} {url}')
                elif status is not None:
                    out(f'- ❌ {status} {url}')
                else:
                    out(f'- ❌ (exception) {url}')
            out()

        # Cloudflare-blocked results (fresh)
        cf_results = [(url, status) for url, status, ok, cf in recheck_results
                      if cf]
        if cf_results:
            out('### Cloudflare-blocked sites (cached for 1 month)')
            out()
            for url, status in cf_results:
                out(f'- 🛡️ {status} {url}')
            out()

    # Cached Cloudflare-blocked sites (not rechecked this run)
    if cached_cloudflare:
        out('### Cloudflare-blocked sites (from cache, still within 1-month TTL)')
        out()
        for url, status in cached_cloudflare:
            out(f'- 🛡️ {status} {url}')
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
    parser.add_argument('--recheck-rate', type=float, default=DEFAULT_RECHECK_RATE,
                        metavar='RPS',
                        help=f'Requests per second for the primp recheck '
                             f'(default: {DEFAULT_RECHECK_RATE}, 0 for no limit)')
    args = parser.parse_args()

    # Determine paths
    if args.ci or os.environ.get('GITHUB_WORKSPACE'):
        base_dir = os.environ['GITHUB_WORKSPACE']
        public_dir = os.path.join(base_dir, 'public')
        config_path = os.path.join(base_dir, CONFIG_FILE)
    else:
        base_dir = SCRIPT_DIR
        public_dir = os.path.join(SCRIPT_DIR, 'public')
        config_path = os.path.join(SCRIPT_DIR, CONFIG_FILE)

    if not os.path.isfile(config_path):
        print(f'Error: {config_path} not found.', file=sys.stderr)
        sys.exit(1)

    config = load_config(config_path)

    # Build ignore entries (ignore + recheck patterns) for LinkChecker
    ignore_patterns = config['ignore'] + config['recheck']
    ignore_entries = _externlinks_from_patterns(ignore_patterns)

    # Load cache and add cached URLs to ignore list
    use_cache = not args.no_cache
    if use_cache:
        cache_path = os.path.join(base_dir, CACHE_FILE)
        cache = load_cache(cache_path)
        renormalize_cache(cache)
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

    # Recheck filtered URLs matching recheck patterns, plus URLs that
    # errored in the main run, using primp (browser impersonation).
    # Error URLs are rechecked regardless of patterns so that
    # Cloudflare-protected targets are detected and cached instead of
    # failing CI until a pattern is added by hand.
    recheck_results = []
    if config['recheck']:
        filtered_urls = extract_ignored_urls(rows, config['silent'],
                                             cached_urls=fresh_cached)
        urls_to_recheck = {u for u in filtered_urls
                           if any(p.search(u) for p in config['recheck'])}
        urls_to_recheck |= {r.base_url for r in rows
                            if _is_error(r) and r.base_url}
        if urls_to_recheck:
            _, recheck_results = recheck_urls(sorted(urls_to_recheck),
                                              rate=args.recheck_rate)

    # Print summary to stdout and, in CI, to GITHUB_STEP_SUMMARY
    step_summary = os.environ.get('GITHUB_STEP_SUMMARY')
    public_ip = fetch_public_ip() if args.ci else None
    if public_ip:
        print(f'Runner IP: {public_ip}')
    if args.ci and step_summary:
        with open(step_summary, 'a', encoding='utf-8') as f:
            # Tees to stdout and the step summary file. Captures f from the
            # enclosing with block, so out is only valid while it is open —
            # print_summary must call it synchronously, not store it.
            def out(s=''):
                print(s, file=sys.stdout)
                print(s, file=f)
            stats = print_summary(rows, config['silent'], out=out,
                                  cached_urls=fresh_cached, public_ip=public_ip,
                                  recheck_results=recheck_results, cache=cache)
    else:
        stats = print_summary(rows, config['silent'], cached_urls=fresh_cached,
                              public_ip=public_ip, recheck_results=recheck_results,
                              cache=cache)

    # Extract ignored URLs if requested
    if args.ignored:
        urls = extract_ignored_urls(rows, config['silent'],
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
        # Add successfully rechecked URLs to the cache
        for url, status, ok, cloudflare in recheck_results:
            if ok:
                cache[url] = {
                    'result': str(status),
                    'cached_at': now.isoformat(),
                }
            elif cloudflare:
                cache[url] = {
                    'result': str(status),
                    'cached_at': now.isoformat(),
                    'cloudflare': True,
                    'ttl_hours': CLOUDFLARE_CACHE_TTL_HOURS,
                }
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
