# Link checker fallback for bot-blocked links

When the primp recheck gets a bot-protection block (Cloudflare, Akamai), the
link cannot be verified live from a datacenter IP. Since the "Detect Akamai
bot blocks" commit, blocked links are cached for a random 30-45 days
(`bot_cache_ttl_range` in `linkchecker-config.yaml`) and re-probed later. The
open question is what to do between re-probes: how to gain confidence that a
blocked link is still alive using current information, rather than an archive
of the past.

## Options evaluated

All options were probed live against the blocked analog.com URLs
(`an-581.html`, `an-0990.html`, `ask-the-applications-engineer-25.html`) on
2026-10-25:

| Option | Evidence | Current or past | Probe result |
|---|---|---|---|
| Site's own sitemap (robots.txt, sitemap index, child sitemaps, URL membership, lastmod) | First-party, site-generated | Current | Works: all probed URLs are listed in analog.com's current sitemaps (`en-app-notes-sitemap.xml`, `en-analog-dialogue-sitemap.xml`), served unprotected from `/media/en/` |
| Headless real browser (Playwright) retry for blocked links | First-party, direct fetch | Current | Not tested; expected high (Akamai Bot Manager is built to pass real browsers; primp lacks only the JS sensor) |
| Residential egress (self-hosted runner on a home connection) | First-party, direct fetch | Current | Not tested; expected high (the block is IP-reputation-based). Security: never expose a home runner to `pull_request` |
| Proxy-as-a-service (Zenrows tested 2026-10-25; ScraperAPI, Bright Data, own VPS untested) | Third-party, direct fetch | Current | Zenrows: passes Cloudflare with `js_render=true` (researchgate -> 200, real page); passes Akamai for analog.com with `js_render=true&premium_proxy=true` (2/2, real page); plain fetch is intermittent (1/4). Paid per request, extra credits for js_render/premium_proxy |
| urlscan.io fresh scan | Third-party, live browser fetch | Current | Key tested 2026-10-25: API works, but the scanner is Akamai-blocked for analog.com (403 "Access Denied") while it passes Cloudflare (researchgate -> 200, real title). Viable for the Cloudflare kind only |
| VirusTotal URL rescan | Third-party, live fetch | Current | Not tested; datacenter fetcher may be blocked |
| W3C checklink | Third-party, live fetch | Current | Inconclusive (returned its form page; likely UA-gated or blocked) |
| Reader proxy (r.jina.ai) | Third-party, live fetch | Current | Eliminated: Akamai blocks it too (403) |
| Sibling resource on an unprotected path (app-note PDF) | First-party, direct fetch | Current | Does not work for analog.com: guessed PDF paths return 404, and the `application-notes/` PDF path is bot-blocked (the unprotected `data-sheets/` area does not cover app notes) |
| Search engine current index | Indirect | Current index, days-weeks lag | Not tested; weak signal |
| Common Crawl recent crawl | Archive | Past (monthly) | No capture for `an-581` in CC-MAIN-2026-43; absence does not mean dead |
| Wayback / Memento (arquivo.pt) | Archive | Past | Works; the baseline this document moves away from |
| No fallback (re-probe in 30-45 days) | None | — | Current behavior |

## Conclusion

1. **Primary fallback: the site's own sitemap.** It is the only option that
   is simultaneously first-party, current, validated against the actual
   blocked URLs, and free. It is also the only *first-party* validated
   option that works for the Akamai-blocked analog.com links: urlscan.io
   and r.jina.ai are Akamai-blocked too.
2. **Live direct fallback: Zenrows** (`js_render=true`, plus
   `premium_proxy=true` for Akamai). The only third-party option validated
   for the Akamai-blocked analog.com links (2/2, real page) and also
   validated for Cloudflare (researchgate -> 200, real page). Paid per
   request with extra credits for js_render/premium_proxy, but with only a
   handful of blocked links per month the cost is negligible. Key in
   Actions secrets. Trade-off vs. the sitemap: paid and third-party, but
   it verifies the actual page (current, direct) rather than sitemap
   membership.
3. **Third-party annotation: urlscan.io** (free API key) for Cloudflare-kind
   blocks (tested: passes Cloudflare, e.g. researchgate returns 200 with the
   real page title). Not usable for Akamai blocks: the scanner gets the same
   403 as we do. Redundant with Zenrows for the Cloudflare kind, but free.
4. **Upgrade path: headless real browser (Playwright).** First-party direct
   verification if preferred over paying per request or relying on sitemap
   membership. Heavier CI (Chromium install, ~1-2 min and ~300 MB), no
   third party.
5. **Safety net: the 30-45 day re-probe stays** regardless of the fallback
   chosen.
6. **Wayback / Common Crawl** remain available as an optional secondary past
   signal, but nothing depends on them.

## Implementation notes for the sitemap fallback

Status: implemented in `linkchecker.py` (`verify_blocked_with_sitemaps`).

- On a bot-block of URL `U` on host `H`: resolve `H`'s sitemap set via
  `robots.txt` -> sitemap index -> child sitemaps, and check whether `U` is
  listed.
- Cache the sitemap set per host (the child sitemap list, under a reserved
  `__sitemaps__<host>` cache key) with the success TTL (7-14 days), so the
  robots.txt and index fetches are not repeated on every cycle. Child
  sitemaps are fetched once per host per run, within the size budget.
- Apply a size budget per host per run (analog.com's largest child sitemap is
  ~1.7 MB; name-matching child sitemaps reduces this).
- Sitemap hit: cache the link as verified (marked `sitemap_verified`,
  reported under "Sitemap-verified" in the summary) with the success TTL
  band (7-14 days), re-verified through the cached sitemap on each cycle.
- Sitemap miss: the link stays bot-blocked (30-45 days). Absence is ambiguous
  (delisted vs. dead), so a miss never fails CI.
- Opportunistic per host: only helps hosts whose sitemaps are reachable.
- Caveat: a sitemap reflects the site's last publish, not literally the
  current second; a link that died yesterday can still be listed.

## Update: connection-level failures (2026-10-25)

The edn.com case turned out to be different from a bot-protection
block: the site is alive (Wayback has 200 snapshots of the root page on
2026-10-19 and 2026-10-21, and Safari/Firefox fingerprints get 200)
but resets connections for the Chrome TLS fingerprint, so the recheck
threw an exception instead of getting an HTTP response. The recheck
now retries failed requests once with a Safari fingerprint, which
edn.com answers with 200 — the link is verified live and cached on the
success cadence. Note: the content still marks the link as a
struck-through historical reference ("now offline"), a note that is
outdated.


## urlscan.io API notes (tested 2026-10-25)

- The `api-key` header is required on both the submit
  (`POST /api/v1/scan/`) and the result (`GET /api/v1/result/{uuid}/`)
  requests; without it the result endpoint answers
  `{"warning": "You're not logged in!"}`.
- Submit with `{"url": ..., "visibility": "unlisted"}` so scans are not
  publicly searchable.
- The result JSON has no `task.status`; poll until `page.status` is present
  (scans complete in ~20-30 s).
- Relevant fields: `page.status` (live HTTP status), `page.title`,
  `page.url` (final URL after redirects), `page.server`, `page.ip`.
- Probe results: an-581 (Akamai) -> 403 "Access Denied" (`AkamaiGHost`,
  scanner IP 23.212.201.43, DE); researchgate figure (Cloudflare) -> 200
  with the real page title.
- Keep the key in GitHub Actions secrets (e.g. `URLSCAN_API_KEY`); never
  commit it. `urlscan_probe.py` reads it from the environment.

## Zenrows API notes (tested 2026-10-25)

- Request: `GET https://api.zenrows.com/v1/?apikey=<key>&url=<url-encoded
  target>` — the key is a query parameter, not a header.
- Useful parameters: `js_render=true` (headless browser, solves JS
  challenges), `premium_proxy=true` (residential proxies). Both cost extra
  credits; a plain request is cheapest.
- Results:
  - example.com (plain) -> 200, real page (key sanity check).
  - an-581 (plain) -> intermittent: 1 success out of 4; failures return
    HTTP 422 `RESP001` "Could not get content".
  - an-581 (`js_render=true`) -> 422; the error suggests enabling premium
    proxies.
  - an-581 (`js_render=true&premium_proxy=true`) -> 200, real page
    ("AN-581: Biasing and Decoupling Op Amps in Single Supply
    Applications"), 2/2 attempts, 8-16 s each.
  - researchgate (plain) -> 422; the error suggests enabling JS rendering.
  - researchgate (`js_render=true`) -> 200, real page (291 KB, ~55 s).
- Timeouts: allow up to ~60-90 s per request. Only probe blocked links (a
  handful per month), so volume and cost stay negligible.
- Keep the key in GitHub Actions secrets (e.g. `ZENROWS_API_KEY`); never
  commit it.

