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

The config file is `.linkcheckerrc` at the repo root. It contains a `PLACEHOLDER`
in the `localwebroot` setting that is replaced at runtime:
- Locally: `linkchecker.sh` replaces it with the local `public/` path
- In CI: the GitHub Actions workflow replaces it with the CI workspace path via `sed`

Settings:
- `check-extern=1` — check external links
- `ssl-verify=1` — verify SSL certificates
- `localwebroot` — resolve absolute URLs (e.g. `/posts/foo.html`) from the local filesystem
- `ignore` — URLs to skip (Cloudflare-protected sites, LinkedIn, Wikimedia)
- `user-agent` — browser-like User-Agent to avoid 403 bot detection

### Ignored sites

The following sites are ignored because they use Cloudflare bot protection (JS challenge)
or rate limiting that no HTTP-based link checker can bypass:

- `www.researchgate.net` — Cloudflare
- `www.hindawi.com` — Cloudflare
- `doi.org` — redirects to Cloudflare-protected sites
- `electronics.stackexchange.com` — Cloudflare
- `www.linkedin.com` — blocks bots
- `upload.wikimedia.org` — rate limits (429)

See `link-test-benchmarks/comparison.md` for the full investigation.

## Local usage

```bash
# Build the site
hugo --minify --baseURL "https://f4inx.github.io/"

# Run LinkChecker via the helper script (output to log file)
./linkchecker.sh /tmp/linkchecker-output.log

# View error summary
grep "Result" /tmp/linkchecker-output.log | sort | uniq -c | sort -rn

# View specific errors
grep -B5 "404 Not Found" /tmp/linkchecker-output.log

# Also produce a list of ignored URLs for manual checking
./linkchecker.sh /tmp/linkchecker-output.log --ignored /tmp/ignored-urls.log
cat /tmp/ignored-urls.log
```

Or run directly (replace PLACEHOLDER first):
```bash
sed "s|file:///PLACEHOLDER/|file://$(pwd | sed 's/ /%20/g')/public/|" .linkcheckerrc > /tmp/lc.conf
linkchecker --config /tmp/lc.conf --check-extern --no-warnings ./public/ > /tmp/linkchecker-output.log 2>&1
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
5. Replaces the `PLACEHOLDER` in `.linkcheckerrc` with the CI workspace path via `sed`,
   then runs LinkChecker with verbose output.
6. Writes a summary to the GitHub Actions step summary, including:
   - Any link errors found
   - A list of ignored links for manual checking
   - Final statistics

The workflow uses `continue-on-error: true` so it is non-blocking — broken links
will be reported in the CI logs but will not prevent deployment.
