#!/usr/bin/env python3
"""Offline unit tests for linkchecker.py.

Covers the cache TTL bands, bot-block detection (Cloudflare/Akamai), the
primp recheck plumbing (with a mocked primp client), the sitemap fallback
for bot-blocked links (with a mocked primp client), and the summary
reporting. No network access required.

Run from the repository root:

    python3 test_linkchecker.py
"""

import gzip
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
    instances = 0

    def __init__(self, *args, **kwargs):
        FakeClient.instances += 1
        self.instance_no = FakeClient.instances

    def get(self, url, timeout=30):
        # The first client (Chrome fingerprint) fails on flaky.example,
        # simulating a site that resets Chrome connections; the retry
        # client (Safari fingerprint) answers it.
        if 'flaky.example' in url and self.instance_no == 1:
            raise RuntimeError('stream error')
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

by_url = {u: (status, ok, block, sitemap)
          for u, status, ok, block, sitemap in results}
check('recheck ok tuple', by_url['https://ok.example/'] == (200, True, None, None))
check('recheck cloudflare tuple',
      by_url['https://cf.example/'] == (403, False, 'cloudflare', None))
check('recheck akamai tuple',
      by_url['https://akamai.example/'] == (403, False, 'akamai', None))
check('recheck exception tuple',
      by_url['https://boom.example/'] == (None, False, None, None))
joined = '\n'.join(lines)
check('recheck lines split cloudflare/akamai',
      '🛡️ Cloudflare |     1' in joined and '🛡️ Akamai |     1' in joined)

# --- recheck_urls retries failed requests with a second fingerprint ---
FakeClient.instances = 0
primp.Client = FakeClient
try:
    _, retry_results = lc.recheck_urls(['https://flaky.example/'], rate=0)
finally:
    primp.Client = real_client
check('chrome-failing url succeeds on safari retry',
      retry_results == [('https://flaky.example/', 200, True, None, None)])
check('retry client was created', FakeClient.instances == 2)
FakeClient.instances = 0
primp.Client = FakeClient
try:
    _, boom_results = lc.recheck_urls(['https://boom.example/'], rate=0)
finally:
    primp.Client = real_client
check('url failing on both fingerprints is an exception',
      boom_results == [('https://boom.example/', None, False, None, None)])
check('retry client reused for second failure', FakeClient.instances == 2)

# --- print_summary: separate Cloudflare/Akamai counts ---
out_lines = []


def collect(s=''):
    out_lines.append(s)


recheck_results = [
    ('https://ok.example/', 200, True, None, None),
    ('https://cf.example/', 403, False, 'cloudflare', None),
    ('https://akamai.example/', 403, False, 'akamai', None),
    ('https://fail.example/', 404, False, None, None),
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
    'https://sv-old.example/': {'result': '403', 'akamai': True,
                                'sitemap_verified': True,
                                'cached_at': datetime.now().isoformat()},
}
lc.print_summary([], [], out=collect2, cache=cache,
                 cached_urls=set(cache))
summary2 = '\n'.join(out_lines2)
check('cached cloudflare row', '🛡️ Cloudflare (cached)       |     1' in summary2)
check('cached akamai row', '🛡️ Akamai (cached)           |     1' in summary2)
check('cached sitemap row',
      '📄 Sitemap-verified (cached)  |     1' in summary2)
check('cached cloudflare section lists entry',
      '- 🛡️ 403 https://cf-old.example/' in summary2)
check('cached akamai section lists entry',
      '- 🛡️ 403 https://akamai-old.example/' in summary2)
check('cached sitemap section lists entry',
      '- 📄 403 https://sv-old.example/' in summary2)
check('cached sitemap entry not in akamai section',
      summary2.count('https://sv-old.example/') == 1)

# --- print_summary: sitemap-verified fresh results ---
out_lines3 = []


def collect3(s=''):
    out_lines3.append(s)


sv_results = [
    ('https://blocked.example/a.html', 403, False, 'akamai', True),
    ('https://blocked.example/missing.html', 403, False, 'akamai', False),
]
lc.print_summary([], [], out=collect3, recheck_results=sv_results)
summary3 = '\n'.join(out_lines3)
check('fresh sitemap row with count 1',
      '📄 Sitemap-verified           |     1' in summary3)
check('fresh sitemap section',
      '### Sitemap-verified bot-blocked links (cached 7-14 days)' in summary3)
check('fresh sitemap section lists verified url',
      '- 📄 403 https://blocked.example/a.html (akamai)' in summary3)
check('unverified block stays in akamai row',
      '🛡️ Akamai blocked             |     1' in summary3)
akamai_section = ''
if '### Akamai-blocked sites (cached 30-45 days)' in summary3:
    akamai_section = summary3.split(
        '### Akamai-blocked sites (cached 30-45 days)')[1].split('###')[0]
check('verified link not in akamai section, unverified is',
      'a.html' not in akamai_section and 'missing.html' in akamai_section)

# --- sitemap helpers ---
locs, is_index = lc._parse_sitemap_locs(
    '<?xml version="1.0"?><urlset><url><loc>https://x.example/a</loc></url>'
    '<url><loc>https://x.example/b</loc></url></urlset>')
check('parse urlset', locs == ['https://x.example/a', 'https://x.example/b']
      and not is_index)
locs, is_index = lc._parse_sitemap_locs(
    '<?xml version="1.0"?><sitemapindex>'
    '<sitemap><loc>https://x.example/s1.xml</loc></sitemap></sitemapindex>')
check('parse index', locs == ['https://x.example/s1.xml'] and is_index)
check('normalize sitemap url',
      lc._normalize_sitemap_url('https://x.example/a/?x=1&amp;y=2')
      == 'https://x.example/a/?x=1&y=2')
check('normalize sitemap url trailing slash',
      lc._normalize_sitemap_url('https://x.example/a/')
      == 'https://x.example/a')

# --- _SitemapFetcher with a mocked primp client ---
class SitemapFakeResponse:
    def __init__(self, content):
        self.status_code = 200
        self.content = content


class SitemapFakeClient:
    calls = []
    pages = {}

    def __init__(self, *args, **kwargs):
        pass

    def get(self, url, timeout=30):
        SitemapFakeClient.calls.append(url)
        content = SitemapFakeClient.pages.get(url)
        if content is None:
            raise RuntimeError('not found')
        return SitemapFakeResponse(content)


gz_xml = gzip.compress(
    b'<urlset><url><loc>https://gz.example/x</loc></url></urlset>')
SitemapFakeClient.pages = {
    'https://gz.example/sitemap.xml': gz_xml,
    'https://fail.example/robots.txt': None,
}
primp.Client = SitemapFakeClient
try:
    fetcher = lc._SitemapFetcher(rate=0)
    check('fetcher gunzips', fetcher.get('https://gz.example/sitemap.xml')
          == '<urlset><url><loc>https://gz.example/x</loc></url></urlset>')
    check('fetcher memoizes',
          fetcher.get('https://gz.example/sitemap.xml')
          == '<urlset><url><loc>https://gz.example/x</loc></url></urlset>'
          and SitemapFakeClient.calls.count('https://gz.example/sitemap.xml') == 1)
    check('fetcher failure returns None',
          fetcher.get('https://fail.example/robots.txt') is None)
finally:
    primp.Client = real_client

# --- verify_blocked_with_sitemaps with a mocked primp client ---
HOST = 'blocked.example'
SitemapFakeClient.calls = []
SitemapFakeClient.pages = {
    f'https://{HOST}/robots.txt': (
        'User-agent: *\n'
        f'Sitemap: https://{HOST}/sitemap_index.xml\n').encode(),
    f'https://{HOST}/sitemap_index.xml': (
        '<?xml version="1.0"?><sitemapindex>'
        f'<sitemap><loc>https://{HOST}/sitemap_a.xml</loc></sitemap>'
        f'<sitemap><loc>https://{HOST}/sitemap_b.xml</loc></sitemap>'
        '</sitemapindex>').encode(),
    f'https://{HOST}/sitemap_a.xml': (
        '<?xml version="1.0"?><urlset>'
        f'<url><loc>https://{HOST}/a.html</loc></url>'
        f'<url><loc>https://{HOST}/b.html</loc></url>'
        '</urlset>').encode(),
    f'https://{HOST}/sitemap_b.xml': (
        '<?xml version="1.0"?><urlset>'
        f'<url><loc>https://{HOST}/c.html</loc></url>'
        '</urlset>').encode(),
}
cfg = lc.load_config(os.path.join(SCRIPT_DIR, 'linkchecker-config.yaml'))


def make_results():
    return [
        (f'https://{HOST}/a.html', 403, False, 'akamai', None),
        (f'https://{HOST}/c.html', 403, False, 'cloudflare', None),
        (f'https://{HOST}/missing.html', 403, False, 'akamai', None),
        ('https://ok.example/', 200, True, None, None),
        ('https://nositemap.example/x', 403, False, 'cloudflare', None),
    ]


primp.Client = SitemapFakeClient
try:
    vcache = {}
    out = lc.verify_blocked_with_sitemaps(make_results(), vcache, cfg, rate=0)
finally:
    primp.Client = real_client
by_url = {u: sitemap for u, status, ok, block, sitemap in out}
check('sitemap hit (akamai, first child)',
      by_url[f'https://{HOST}/a.html'] is True)
check('sitemap hit (cloudflare, second child)',
      by_url[f'https://{HOST}/c.html'] is True)
check('sitemap miss (not listed)',
      by_url[f'https://{HOST}/missing.html'] is False)
check('sitemap None for ok link', by_url['https://ok.example/'] is None)
check('sitemap None for host without sitemap',
      by_url['https://nositemap.example/x'] is None)
check('sitemap set cached per host',
      vcache.get(f'__sitemaps__{HOST}', {}).get('children')
      == [f'https://{HOST}/sitemap_a.xml', f'https://{HOST}/sitemap_b.xml'])
check('cached sitemap set has success ttl',
      7 * 24 <= vcache[f'__sitemaps__{HOST}']['ttl_hours'] <= 14 * 24)
n_calls_first = len(SitemapFakeClient.calls)

# second cycle: cached sitemap set must skip robots.txt and the index
primp.Client = SitemapFakeClient
try:
    out2 = lc.verify_blocked_with_sitemaps(make_results(), vcache, cfg, rate=0)
finally:
    primp.Client = real_client
calls_second = SitemapFakeClient.calls[n_calls_first:]
check('second cycle reuses cached sitemap set',
      f'https://{HOST}/robots.txt' not in calls_second
      and f'https://{HOST}/sitemap_index.xml' not in calls_second)
check('second cycle still fetches children',
      calls_second.count(f'https://{HOST}/sitemap_a.xml') == 1)
check('second cycle same verdicts',
      {u: s for u, s, ok, b, s in out2}
      == {u: s for u, s, ok, b, s in out})

# no blocked links -> no fetches at all
SitemapFakeClient.calls = []
primp.Client = SitemapFakeClient
try:
    out3 = lc.verify_blocked_with_sitemaps(
        [('https://ok.example/', 200, True, None, None)], {}, cfg, rate=0)
finally:
    primp.Client = real_client
check('no blocked links means no sitemap fetches',
      SitemapFakeClient.calls == [] and out3[0][4] is None)

# size budget: an over-cap child sitemap is not parsed
big_child = ('<?xml version="1.0"?><urlset>'
             + ''.join(f'<url><loc>https://{HOST}/u{i}.html</loc></url>'
                       for i in range(500))
             + '</urlset>').encode()
SitemapFakeClient.pages = {
    f'https://{HOST}/robots.txt':
        f'Sitemap: https://{HOST}/big.xml\n'.encode(),
    f'https://{HOST}/big.xml': big_child,
}
real_cap = lc.SITEMAP_MAX_BYTES_PER_SITEMAP
lc.SITEMAP_MAX_BYTES_PER_SITEMAP = 100
primp.Client = SitemapFakeClient
try:
    out4 = lc.verify_blocked_with_sitemaps(
        [(f'https://{HOST}/u0.html', 403, False, 'akamai', None)], {}, cfg,
        rate=0)
finally:
    primp.Client = real_client
    lc.SITEMAP_MAX_BYTES_PER_SITEMAP = real_cap
check('over-cap child sitemap is skipped (miss, never fails)',
      out4[0][4] is False)

# --- TTL bands (regression) ---
cache5 = {}
now = datetime.now()
lc.update_cache(cache5, [ud(f'https://site{i}.com/') for i in range(100)], now)
ttls = [e['ttl_hours'] for e in cache5.values()]
check('success ttls within [7,14] days', all(7 * 24 <= t <= 14 * 24 for t in ttls))
check('bot_cache_ttl_range from config', cfg['bot_cache_ttl_range'] == (30 * 24, 45 * 24))

print()
print('FAILURES:', fails if fails else 'none')
sys.exit(1 if fails else 0)
