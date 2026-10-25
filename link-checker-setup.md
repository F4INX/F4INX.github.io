# Link checker setup

The site uses [LinkChecker](https://github.com/linkchecker/linkchecker) for link checking,
both locally and in CI (GitHub Actions). LinkChecker was chosen over lychee and htmltest
after benchmarking — see `link-test-benchmarks/comparison.md` for details.

## Why LinkChecker?

- Handles HTTP/2 correctly (lychee and htmltest both fail on analog.com and edn.com)
- Custom User-Agent reduces 403 errors (lychee has no User-Agent support)
- `localwebroot` setting resolves absolute URLs from the local filesystem (zero false positives)
- 52s runtime (vs 55s for lychee, 5m24s for htmltest)

## Installation

### Debian/WSL

```bash
sudo apt update && sudo apt install -y linkchecker
```

Verify:
```bash
linkchecker --version
```

## Configuration

LinkChecker is configured programmatically in `linkchecker.py` via its Python
API. All URL patterns and tunables are configured in a single YAML file,
`linkchecker-config.yaml`.

Pattern sections (one regex per line):

- `ignore` — URLs skipped by LinkChecker and never rechecked (Cloudflare,
  bot protection, rate limiting)
- `recheck` — URLs skipped by LinkChecker but rechecked afterwards with
  `primp` (browser impersonation)
- `silent` — URLs hidden from the summary's filtered/ignored list (e.g.
  `data:` URIs)

Scalar settings:

- `recheck_rate` — requests per second for the primp recheck (0.5)
- `cache_ttl_range` — cache TTL range in days for successfully checked
  external links; a random TTL is drawn from this range for each link
  (7-14), so rechecks spread evenly over time instead of happening in a
  burst on every run
- `bot_cache_ttl_range` — cache TTL range in days for bot-blocked links
  (Cloudflare, Akamai); blocked links are re-probed after a random TTL
  drawn from this range (30-45)

Other settings are set directly in code:

- `checkextern = True` — check external links
- `sslverify` — on by default (LinkChecker default)
- `localwebroot` — set to the `public/` path in file mode, unused in server mode
- `useragent` — browser-like User-Agent to avoid 403 bot detection

### Filtered sites

Sites in the `ignore` list are skipped and never rechecked; sites in the
`recheck` list are skipped by LinkChecker but rechecked afterwards with
primp (browser impersonation). Notable entries:

- `ignore`: `www.linkedin.com` (Cloudflare challenge), `fr.rs-online.com`
  (Akamai bot protection, silent redirects)
- `recheck`: `www.analog.com` (Akamai blocks article pages for datacenter
  IPs), `www.edn.com`, `www.everythingrf.com` (Cloudflare),
  `product.tdk.com`, `upload.wikimedia.org` (rate limits),
  `web.archive.org`, `www.researchgate.net` (Cloudflare),
  `www.hindawi.com` (Cloudflare), `electronics.stackexchange.com`
  (Cloudflare), `mcalc.sourceforge.net` (Cloudflare),
  `dx.doi.org/10.1155/2013/232317` (DOI redirect to a Cloudflare-protected
  site)

See `link-test-benchmarks/comparison.md` for the full investigation.

## Local usage

```bash
# Build the site
hugo --minify --baseURL "https://f4inx.github.io/"

# Run LinkChecker via the helper script (output to log file)
./linkchecker.py > /tmp/linkchecker-output.log

# View error summary
grep "Result" /tmp/linkchecker-output.log | sort | uniq -c | sort -rn

# View specific errors
grep -B5 "404 Not Found" /tmp/linkchecker-output.log

# Also produce a list of ignored URLs for manual checking
./linkchecker.py --ignored /tmp/ignored-urls.log > /tmp/linkchecker-output.log
cat /tmp/ignored-urls.log
```

Note: LinkChecker takes ~50s to run. Always write output to a log file first,
then process the log file. This allows re-running different grep/sort commands
on the same output without re-running LinkChecker.

## CI usage (GitHub Actions)

The workflow is defined in `.github/workflows/link-check.yml`. It runs on
pushes to `master`, on pull requests, on demand, and on a daily schedule
(06:00 UTC). Each run:

1. Checks out the repo
2. Installs Hugo
3. Builds the site with `hugo --minify`
4. Installs the Python dependencies in a venv (`requirements.txt`,
   `requirements-pinned.txt`)
5. Runs `python3 linkchecker.py --ci` which:
   - Configures LinkChecker via its Python API and `linkchecker-config.yaml`
   - Runs LinkChecker and collects results via a custom logger
   - Rechecks filtered and failed links with `primp` (browser
     impersonation, paced by `recheck_rate`), and verifies bot-blocked
     links against their host's current sitemap (see
     `link-checker-fallback.md`)
   - Writes a summary to the GitHub Actions step summary, including:
     - Status table (total, OK, redirects, filtered, ignored, warnings,
       errors, rechecked, Cloudflare-blocked, Akamai-blocked,
       sitemap-verified)
     - Any link errors and warnings found
     - Redirects (original URL --> final URL)
     - Rechecked links, bot-blocked sites (Cloudflare, Akamai), and
       sitemap-verified links
     - A list of ignored links for manual checking
     - Final statistics

External-link results are cached in `.linkchecker-cache.json`, persisted
between runs via the GitHub Actions cache and a 7-day artifact:
successful links are skipped for a random 7-14 days, bot-blocked links
(Cloudflare, Akamai) for a random 30-45 days, and entries older than
60 days are pruned.

The check is blocking: the job fails when errors or warnings are found.
Recheck errors and bot-blocked sites are reported but do not fail the job.
