# Link checker comparison

Comparison of three link checkers for the f4inx.github.io Hugo site.

## Tools compared

| Feature | lychee | htmltest | LinkChecker |
|---------|--------|----------|-------------|
| Version | 0.24.2 | 0.17.0 | 10.6.0 |
| Language | Rust | Go | Python |
| GitHub Action | `lycheeverse/lychee-action@v2` | `manuchimera/htmltest-action` | None official |
| Config file | `.lycheeignore` (auto-detected) | `htmltest.yml` | `.linkcheckerrc` |
| Custom User-Agent | No | Yes (`HTTPHeaders` in config) | Yes (`--user-agent` or config) |
| HTTP/2 handling | Rust `reqwest` (strict) | Go `net/http` (robust) | Python `requests` (robust) |
| Ignore URLs | Regex patterns in `.lycheeignore` | `IgnoreURLs` in config | `ignore` in config |
| Checks alt text | No | Yes | No |
| Checks anchors | No | Yes | Yes |
| Output formats | compact, detailed, json, junit, markdown | text | text, html, sql, xml, gml, dot, csv |

## Installation

All three tools are installed in `link-test-benchmarks/bin/` for reproducible benchmarking.

### lychee

```bash
mkdir -p link-test-benchmarks/bin/lychee
curl -sL "https://github.com/lycheeverse/lychee/releases/latest/download/lychee-x86_64-unknown-linux-gnu.tar.gz" -o /tmp/lychee-dl.tar.gz
tar xzf /tmp/lychee-dl.tar.gz --strip-components=1 -C /tmp/
cp /tmp/lychee link-test-benchmarks/bin/lychee/lychee
chmod +x link-test-benchmarks/bin/lychee/lychee
```

### htmltest

```bash
mkdir -p link-test-benchmarks/bin/htmltest
curl -sL "https://github.com/wjdp/htmltest/releases/download/v0.17.0/htmltest_0.17.0_linux_amd64.tar.gz" -o /tmp/htmltest-dl.tar.gz
tar xzf /tmp/htmltest-dl.tar.gz -C link-test-benchmarks/bin/htmltest/
chmod +x link-test-benchmarks/bin/htmltest/htmltest
```

### LinkChecker

```bash
python3 -m venv link-test-benchmarks/bin/linkchecker
link-test-benchmarks/bin/linkchecker/bin/pip install LinkChecker
```

## Configuration files

All three configs have NO ignored URLs. The goal is to test which tool can handle HTTP/2 issues and 403 bot detection on its own.

- `lycheeignore-bench` — empty (no ignores)
- `htmltest-bench.yml` — htmltest config with browser User-Agent, no `IgnoreURLs`
- `linkcheckerrc-bench` — LinkChecker config with browser User-Agent and `localwebroot`, no `ignore`

LinkChecker uses `localwebroot` to resolve absolute URLs (e.g. `/posts/foo.html`) from the local filesystem instead of trying to find them at the filesystem root. The path must use URL syntax with forward slashes and a trailing slash:

```ini
localwebroot=file:///path/to/f4inx.github.io/public/
```

## Running the benchmarks

```bash
# Build the site first
hugo --minify --baseURL "https://f4inx.github.io/"

# lychee (temporarily remove root .lycheeignore to avoid auto-detection)
mv .lycheeignore .lycheeignore.bak
link-test-benchmarks/bin/lychee/lychee --base-url https://f4inx.github.io/ --no-progress --exclude-file link-test-benchmarks/lycheeignore-bench "./public/**/*.html"
mv .lycheeignore.bak .lycheeignore

# htmltest (do NOT use -s flag, it skips external links)
link-test-benchmarks/bin/htmltest/htmltest -c link-test-benchmarks/htmltest-bench.yml ./public

# LinkChecker
link-test-benchmarks/bin/linkchecker/bin/linkchecker --config link-test-benchmarks/linkcheckerrc-bench --check-extern --no-warnings ./public/
```

## Benchmark results

### Summary

| Metric | lychee | htmltest | LinkChecker |
|--------|--------|----------|-------------|
| Total time | 55s | 5m24s | 52s |
| Total links checked | 1879 | 29 documents | 720 |
| Unique links | 515 | unknown | 664 |
| Total errors | 21 | 228 | 10 |
| Excluded/ignored | 0 | 0 | 0 |
| HTTP/2 errors (analog.com) | 10 | 10 (timeouts) | 0 (passed) |
| HTTP/2 errors (edn.com) | 2 | 2 (timeouts) | 0 (passed) |
| 403 errors | 8 | 13 | 5 |
| 500 errors | 1 | 1 | 0 |
| 404 errors | 0 | 0 | 4 |
| 202 (doi.org) | 0 | 17 | 0 |
| Timeout errors | 1 (finetune.co.jp) | 0 | 0 |
| Internal false positives | 0 | 0 | 0 (fixed with localwebroot) |
| Alt text warnings | N/A | ~120 | N/A |
| Completed | Yes | Yes | Yes |

### HTTP/2 issue resolution

| Site | lychee | htmltest | LinkChecker |
|------|--------|----------|-------------|
| analog.com (10 links) | HTTP/2 protocol error | Timeout | Passed |
| edn.com (2 links) | HTTP/2 protocol error | Timeout | Passed |

Only LinkChecker handles HTTP/2 with analog.com and edn.com correctly.

### 403 bot detection

| Site | lychee | htmltest | LinkChecker |
|------|--------|----------|-------------|
| researchgate.net (2 links) | 403 | 403 | 403 |
| hindawi.com (3 links) | 403 | 403 | 403 |
| rs-online.com (6 links) | 403 | 403 | 0 (passed) |
| product.tdk.com (1 link) | not in content | 403 | not in content |
| mcalc.sourceforge.net (1 link) | not in content | 403 | not in content |
| electronics.stackexchange.com (1 link) | 403 | 403 | 403 |
| doi.org (17 links) | 403 | 202 (accepted) | 403 |
| Total 403s | 8 | 13 | 5 |

The custom User-Agent in LinkChecker helped with rs-online.com but not with researchgate.net, hindawi.com, or electronics.stackexchange.com. htmltest's User-Agent did not prevent 403s. lychee has no User-Agent support.

### Detailed analysis

#### lychee

- Completed in 55s
- 10x HTTP/2 protocol errors on analog.com (confirmed bug in Rust reqwest)
- 2x HTTP/2 protocol errors on edn.com (same issue)
- 8x 403 Forbidden (researchgate, hindawi, rs-online, stackexchange)
- 1x 500 on web.archive.org (transient)
- 1x timeout on finetune.co.jp (site is dead)
- No custom User-Agent support
- No internal false positives
- Does not check alt text

#### htmltest

- Completed in 5m24s — very slow
- 10x timeouts on analog.com (HTTP/2 issue not resolved)
- 2x timeouts on edn.com (same)
- 13x 403 Forbidden despite custom User-Agent
- 17x 202 from doi.org (htmltest treats these as errors; lychee and LinkChecker accept them)
- 1x 500 on web.archive.org (transient)
- Also found ~120 alt text/alt attribute issues (not link errors)
- 1x 503 on live site (transient)
- Custom User-Agent did not prevent most 403s

#### LinkChecker

- Completed in 52s
- HTTP/2 issue RESOLVED: all analog.com and edn.com links passed
- 5x 403 Forbidden (researchgate, hindawi, stackexchange) — User-Agent helped for rs-online.com and product.tdk.com but not all sites
- 4x 404 errors (section index pages `/posts/`, `/details/`, `/misc/` that don't exist as standalone pages)
- 1x unrendered Jekyll template tag in CSS (`f4inx-black.svg | absolute_url}}`)
- 0 internal false positives (fixed with `localwebroot` setting)
- Custom User-Agent partially helped with 403s

## Conclusion

- **LinkChecker** is the only tool that handles the HTTP/2 issue with analog.com and edn.com. The custom User-Agent also reduces 403 errors (5 vs 8 for lychee, 13 for htmltest). With the `localwebroot` setting, it has zero false positive internal errors. Only 10 real errors remain, all of which are genuine issues (403 bot blocks, 404 section pages, unrendered template tag).
- **lychee** is the fastest, but has 12 HTTP/2 errors and 8 403 errors with no way to set a custom User-Agent.
- **htmltest** is the slowest (5m24s), does not resolve the HTTP/2 issue, and has the most 403 errors despite a custom User-Agent. It is the only tool that checks alt text.

### Recommendation

**LinkChecker** is the best tool for this site. It handles HTTP/2 correctly, reduces 403 errors with a custom User-Agent, and with `localwebroot` produces zero false positives. The only downside is the lack of an official GitHub Action, but it can be run via a simple shell step in a workflow.

**lychee** remains a good fallback with `.lycheeignore` workarounds, as it is the fastest and has the best GitHub Action integration.

**htmltest** is not suitable as the primary external link checker due to its slowness and inability to resolve HTTP/2 or 403 issues. It could be used alongside lychee for internal-only checks and alt text validation.

## 403 bot protection investigation

### Which sites return 403?

All remaining 403 errors (across all three tools) come from sites behind Cloudflare or Akamai bot protection:

| Site | Protection | 403 with all tools? | 403 with User-Agent? |
|------|-----------|---------------------|---------------------|
| electronics.stackexchange.com | Cloudflare | Yes | Yes |
| www.researchgate.net | Cloudflare | Yes | Yes |
| www.hindawi.com | Cloudflare | Yes | Yes |
| fr.rs-online.com | Akamai | Yes | No (LinkChecker passed) |
| product.tdk.com | Unknown | Yes | No (LinkChecker passed) |
| doi.org | Various | Yes | Yes |

### Can 403 from an existing page be distinguished from a 403 from a non-existing page?

No. Testing with curl on Cloudflare-protected sites shows that both existing and non-existing pages return the same 403 with `cf-mitigated: challenge`:

```
# Existing page (stackexchange)
HTTP/2 403
cf-mitigated: challenge
content-length: 5635

# Non-existing page (stackexchange)
HTTP/2 403
cf-mitigated: challenge
content-length: 5412
```

The `content-length` differs slightly (because the challenge HTML includes the requested URL), but the HTTP status code and headers are identical. Cloudflare blocks the request at the edge before it reaches the origin server, so the origin never checks whether the page exists.

The same behavior was observed on researchgate.net.

### Can full browser headers bypass the 403?

No. Testing with curl using a complete set of browser headers (User-Agent, Accept, Accept-Language, Accept-Encoding, Sec-CH-UA, Sec-CH-UA-Mobile, Sec-CH-UA-Platform, Sec-Fetch-Dest, Sec-Fetch-Mode, Sec-Fetch-Site, Sec-Fetch-User, Upgrade-Insecure-Requests, Connection) still returns 403. The response body is Cloudflare's "Just a moment..." JavaScript challenge page:

```html
<title>Just a moment...</title>
<noscript>Enable JavaScript and cookies to continue</noscript>
```

Cloudflare serves a JS challenge that must be executed in a browser to compute a token, set a `cf_clearance` cookie, and redirect to the actual page. No combination of HTTP headers can bypass this — it requires a JavaScript engine.

### Conclusion on 403 handling

- Custom User-Agent helps with some sites (rs-online.com, product.tdk.com) but not with Cloudflare-protected sites (stackexchange, researchgate, hindawi)
- Cloudflare's `cf-mitigated: challenge` requires JavaScript execution to pass — no HTTP-based link checker can solve this, even with full browser headers
- There is no way to distinguish existing vs non-existing pages behind Cloudflare bot protection
- The only options are:
  1. Ignore these URLs in the config (accept that they cannot be checked automatically)
  2. Use a headless browser that can solve the JS challenge (overly complex for link checking)
  3. Periodically manually check these links in a real browser
