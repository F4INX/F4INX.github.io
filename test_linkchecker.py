#!/usr/bin/env python3
"""Offline unit tests for linkchecker.py.

Covers the cache TTL bands, bot-block detection (Cloudflare/Akamai), the
primp recheck plumbing (with a mocked primp client), and the summary
reporting. No network access required.

Run from the repository root:

    python3 test_linkchecker.py
"""

import os
import sys
import types
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

import linkchecker as lc


def ud(base_url='', url='', result='200 OK', valid=True, warnings=None):
    return types.SimpleNamespace(base_url=base_url, url=url or base_url,
                                 result=result, valid=valid,
                                 warnings=warnings or [])


fails = []


def check(name, cond):
    print(('PASS' if cond else 'FAIL'), name)
    if not cond:
        fails.append(name)


# --- _is_cloudflare_block (unchanged) ---
check('cloudflare 403 is block', lc._is_cloudflare_block(403, {'server': 'Cloudflare'}))
check('cloudflare 503 is block', lc._is_cloudflare_block(503, {'server': 'cloudflare'}))
check('cf-mitigated header is block',
      lc._is_cloudflare_block(403, {'cf-mitigated': 'challenge'}))
check('plain 403 is not', not lc._is_cloudflare_block(403, {'server': 'nginx'}))

# --- _is_akamai_block ---
check('akamai 403 is block', lc._is_akamai_block(403, {'server': 'AkamaiGHost'}))
check('akamai 503 is block', lc._is_akamai_block(503, {'server': 'akamaighost'}))
check('akamai 200 is not', not lc._is_akamai_block(200, {'server': 'AkamaiGHost'}))
check('akamai storage 403 is not (exact match)',
      not lc._is_akamai_block(403, {'server': 'AkamaiNetStorage'}))
check('edgesuite body 403 is block',
      lc._is_akamai_block(403, {'server': 'nginx'},
                          '<HTML>Access Denied ... errors.edgesuite.net/18 ...'))
check('plain 403 without body marker is not',
      not lc._is_akamai_block(403, {'server': 'nginx'}, '<HTML>Forbidden</HTML>'))
check('plain 200 is not', not lc._is_akamai_block(200, {'server': 'nginx'}))

# --- _is_bot_block: main function dispatches to both sub-functions ---
check('bot block returns cloudflare',
      lc._is_bot_block(403, {'server': 'cloudflare'}) == 'cloudflare')
check('bot block returns cloudflare via cf-mitigated',
      lc._is_bot_block(403, {'cf-mitigated': 'challenge'}) == 'cloudflare')
check('bot block returns akamai',
      lc._is_bot_block(403, {'server': 'AkamaiGHost'}) == 'akamai')
check('bot block returns akamai via body',
      lc._is_bot_block(403, {'server': 'nginx'},
                       'errors.edgesuite.net/18') == 'akamai')
check('bot block returns None for 200',
      lc._is_bot_block(200, {'server': 'nginx'}) is None)
check('bot block returns None for plain 403',
      lc._is_bot_block(403, {'server': 'nginx'}) is None)

# --- recheck_urls with a monkeypatched primp client ---
import primp


class FakeResponse:
    def __init__(self, status, headers, text=''):
        self.status_code = status
        self.headers = headers
        self.text = text


class FakeClient:
    def __init__(self, *args, **kwargs):
        pass

    def get(self, url, timeout=30):
        if 'cf.example' in url:
            return FakeResponse(403, {'server': 'cloudflare'})
        if 'akamai.example' in url:
            return FakeResponse(403, {'server': 'AkamaiGHost'},
                                'Access Denied errors.edgesuite.net/18')
        if 'boom.example' in url:
            raise RuntimeError('connection reset')
        return FakeResponse(200, {'server': 'nginx'})


real_client = primp.Client
primp.Client = FakeClient
try:
    lines, results = lc.recheck_urls(
        ['https://ok.example/', 'https://cf.example/',
         'https://akamai.example/', 'https://boom.example/'], rate=0)
finally:
    primp.Client = real_client

by_url = {u: (status, ok, block) for u, status, ok, block in results}
check('recheck ok tuple', by_url['https://ok.example/'] == (200, True, None))
check('recheck cloudflare tuple',
      by_url['https://cf.example/'] == (403, False, 'cloudflare'))
check('recheck akamai tuple',
      by_url['https://akamai.example/'] == (403, False, 'akamai'))
check('recheck exception tuple',
      by_url['https://boom.example/'] == (None, False, None))
joined = '\n'.join(lines)
check('recheck lines split cloudflare/akamai',
      '🛡️ Cloudflare |     1' in joined and '🛡️ Akamai |     1' in joined)

# --- print_summary: separate Cloudflare/Akamai counts ---
out_lines = []


def collect(s=''):
    out_lines.append(s)


recheck_results = [
    ('https://ok.example/', 200, True, None),
    ('https://cf.example/', 403, False, 'cloudflare'),
    ('https://akamai.example/', 403, False, 'akamai'),
    ('https://fail.example/', 404, False, None),
]
lc.print_summary([], [], out=collect, recheck_results=recheck_results)
summary = '\n'.join(out_lines)
check('summary has cloudflare row with count 1',
      '🛡️ Cloudflare blocked        |     1' in summary)
check('summary has akamai row with count 1',
      '🛡️ Akamai blocked             |     1' in summary)
check('summary has recheck errors row with count 1',
      '❌ Recheck errors             |     1' in summary)
check('summary has cloudflare section',
      '### Cloudflare-blocked sites (cached 30-45 days)' in summary)
check('summary has akamai section',
      '### Akamai-blocked sites (cached 30-45 days)' in summary)
check('summary lists akamai url under akamai section',
      '- 🛡️ 403 https://akamai.example/' in summary)

# --- print_summary: cached entries split per kind ---
out_lines2 = []


def collect2(s=''):
    out_lines2.append(s)


cache = {
    'https://cf-old.example/': {'result': '403', 'cloudflare': True,
                                'cached_at': datetime.now().isoformat()},
    'https://akamai-old.example/': {'result': '403', 'akamai': True,
                                    'cached_at': datetime.now().isoformat()},
}
lc.print_summary([], [], out=collect2, cache=cache,
                 cached_urls=set(cache))
summary2 = '\n'.join(out_lines2)
check('cached cloudflare row', '🛡️ Cloudflare (cached)       |     1' in summary2)
check('cached akamai row', '🛡️ Akamai (cached)           |     1' in summary2)
check('cached cloudflare section lists entry',
      '- 🛡️ 403 https://cf-old.example/' in summary2)
check('cached akamai section lists entry',
      '- 🛡️ 403 https://akamai-old.example/' in summary2)

# --- TTL bands (regression) ---
cache3 = {}
now = datetime.now()
lc.update_cache(cache3, [ud(f'https://site{i}.com/') for i in range(100)], now)
ttls = [e['ttl_hours'] for e in cache3.values()]
check('success ttls within [7,14] days', all(7 * 24 <= t <= 14 * 24 for t in ttls))
cfg = lc.load_config(os.path.join(SCRIPT_DIR, 'linkchecker-config.yaml'))
check('bot_cache_ttl_range from config', cfg['bot_cache_ttl_range'] == (30 * 24, 45 * 24))

print()
print('FAILURES:', fails if fails else 'none')
sys.exit(1 if fails else 0)
