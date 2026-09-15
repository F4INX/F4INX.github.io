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
API. All URL patterns are configured in a single YAML file,
`linkchecker-config.yaml`, with three sections:

- `ignore` — URLs skipped by LinkChecker and never rechecked (Cloudflare,
  bot protection, rate limiting)
- `recheck` — URLs skipped by LinkChecker but rechecked afterwards with
  `primp` (browser impersonation)
- `silent` — URLs hidden from the summary's filtered/ignored list (e.g.
  `data:` URIs)

Other settings are set directly in code:

- `checkextern = True` — check external links
- `sslverify` — on by default (LinkChecker default)
- `localwebroot` — set to the `public/` path in file mode, unused in server mode
- `useragent` — browser-like User-Agent to avoid 403 bot detection

### Ignored sites

- `www.researchgate.net` — Cloudflare
- `www.hindawi.com` — Cloudflare
- `electronics.stackexchange.com` — Cloudflare
- `www.linkedin.com` — blocks bots
- `upload.wikimedia.org` — rate limits (429)

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

The workflow is defined in `.github/workflows/link-check.yml`. It:

1. Checks out the repo
2. Installs Hugo
3. Builds the site with `hugo --minify`
4. Installs LinkChecker via `apt-get`
5. Runs `python3 linkchecker.py --ci` which:
   - Configures LinkChecker via its Python API (no config file needed)
   - Runs LinkChecker and collects results via a custom logger
   - Writes a summary to the GitHub Actions step summary, including:
     - Status table (total, OK, redirects, filtered, ignored, errors)
     - Any link errors found
     - Redirects (original URL --> final URL)
     - A list of ignored links for manual checking
     - Final statistics

The workflow uses `continue-on-error: true` so it is non-blocking — broken links
will be reported in the CI logs but will not prevent deployment.
