#!/usr/bin/env python3
"""Probe URLs through urlscan.io and print what its browser got back.

Used to test whether a bot-protected URL can be verified live via
urlscan.io (see link-checker-fallback.md). The API key is read from the
URLSCAN_API_KEY environment variable — never hardcode it.

Usage:

    URLSCAN_API_KEY=... python3 urlscan_probe.py <url> [url ...]

For each URL, prints the live HTTP status, page title, server header, and
final URL after redirects. Scans are submitted with "unlisted" visibility
so they are not publicly searchable.
"""

import json
import os
import sys
import time
import urllib.request

API = 'https://urlscan.io/api/v1'
POLL_INTERVAL_SECONDS = 10
POLL_ATTEMPTS = 30


def api_request(path, key, payload=None):
    """Call the urlscan.io API. The api-key header is required on every
    request, including result retrieval."""
    req = urllib.request.Request(API + path)
    req.add_header('api-key', key)
    data = None
    if payload is not None:
        req.add_header('Content-Type', 'application/json')
        data = json.dumps(payload).encode()
    with urllib.request.urlopen(req, data=data, timeout=30) as resp:
        return json.load(resp)


def probe(url, key):
    result = api_request('/scan/', key, {'url': url, 'visibility': 'unlisted'})
    uuid = result['uuid']
    print(f'{url}')
    print(f'  scan: {result["result"]}')
    # The result JSON has no task.status field; poll until page.status
    # is present (scans complete in ~20-30 s).
    for _ in range(POLL_ATTEMPTS):
        time.sleep(POLL_INTERVAL_SECONDS)
        try:
            data = api_request(f'/result/{uuid}/', key)
        except Exception:
            continue
        page = data.get('page', {})
        if page.get('status'):
            print(f'  status:  {page["status"]}')
            print(f'  title:   {page.get("title")}')
            print(f'  server:  {page.get("server")}')
            print(f'  final:   {page.get("url")}')
            return page['status']
    print('  scan did not finish in time')
    return None


def main():
    key = os.environ.get('URLSCAN_API_KEY')
    if not key:
        print('Error: set URLSCAN_API_KEY in the environment.', file=sys.stderr)
        sys.exit(1)
    urls = sys.argv[1:]
    if not urls:
        print(__doc__)
        sys.exit(1)
    for url in urls:
        probe(url, key)


if __name__ == '__main__':
    main()
