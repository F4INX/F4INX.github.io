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
| Proxy-as-a-service (ScraperAPI, Bright Data, own VPS egress) | Third-party, direct fetch | Current | Not tested for Akamai; residential pools likely pass |
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
   blocked URLs, and free. This is also the only validated option that works
   for the Akamai-blocked analog.com links: urlscan.io and r.jina.ai are
   Akamai-blocked too.
2. **Upgrade path: headless real browser (Playwright).** If direct page
   verification is preferred over sitemap membership. Heavier CI (Chromium
   install, ~1-2 min and ~300 MB), no third party.
3. **Third-party annotation: urlscan.io** (free API key) for Cloudflare-kind
   blocks (tested: passes Cloudflare, e.g. researchgate returns 200 with the
   real page title). Not usable for Akamai blocks: the scanner gets the same
   403 as we do.
4. **Safety net: the 30-45 day re-probe stays** regardless of the fallback
   chosen.
5. **Wayback / Common Crawl** remain available as an optional secondary past
   signal, but nothing depends on them.

## Implementation notes for the sitemap fallback

- On a bot-block of URL `U` on host `H`: resolve `H`'s sitemap set via
  `robots.txt` -> sitemap index -> child sitemaps, and check whether `U` is
  listed.
- Cache the sitemap set per host with the success TTL (7-14 days); sitemaps
  change slowly, so one fetch per host per run is enough.
- Apply a size budget per host per run (analog.com's largest child sitemap is
  ~1.7 MB; name-matching child sitemaps reduces this).
- Sitemap hit: cache the link as verified with the success TTL band
  (7-14 days), re-verified through the cached sitemap on each cycle.
- Sitemap miss: the link stays bot-blocked (30-45 days). Absence is ambiguous
  (delisted vs. dead), so a miss never fails CI.
- Opportunistic per host: only helps hosts whose sitemaps are reachable.
- Caveat: a sitemap reflects the site's last publish, not literally the
  current second; a link that died yesterday can still be listed.

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

