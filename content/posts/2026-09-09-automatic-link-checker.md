---
title: "Automatic link checker"
date: 2026-09-09
lastmod: 2026-09-09
categories: [Site, Meta]
url: /posts/automatic-link-checker.html
excerpt: "Broken links are a common problem. An automatic link checker was implemented for this website."
related_posts:
  - "Gönül's website is awesome"
  - "Switch to Hugo"
---

Broken links are a common problem, particularly for a website which is already old and of medium size, which is an annoyance for both visitors, for search engine optimisation, and for webmasters. While there are good tools available to check this point, it would be better to have something entirely automatic, so a webmaster does not even have to think about this point.

To handle this issue, I configured a github action which check for broken link 1/ when pushing a new version of the website and 2/ time to time to avoid link rot.

## Choice of the link checker tool

A first version of the link checker system used the lychee link checker because it was an easy pick with a ready-made github action. However, it handled poorly some edge case like delayed answers so I had to choose another tool.

After some benchmarks, I settle for a tool called simply LinkChecker, written in Python and mature.

## Wrapper script

In addition to the mere LinkChecker program, I needed some convenience scripts to:

* Handling the different configuration between my computer (WSL) and the github CI.

* Have a shortcut to avoid repeating the flags of LinkChecker.

* Generating a summary with statistics, redirects, and a list of ignored links to manually check time to time.

* Avoid putting too much stuff into the action files.

At the beginning, there were several bash scripts using grep/sed/awk. Then for CSV parsing the bash scripts used inline Python. Then I reworked these to use only a single Python script.

## GitHub action file

The GitHub action file allows to check for broken links 1/ when changes are made and 2/ time to time to avoid link rot. Additionnally, GitHub sends me an email when this action fails so I'm warned that I have to update links.

## Ignored links

According to the last statistics, 26 links are ignored, belonging to the following cases:

* Cloudflare protected sites which prevents bots to check them.

* LinkedIn who has also a bot protection.

* Wikimedia which has a rate-limitation. Note that currently LinkChecker has no per-site rate-limitation.

* archive.org which for unclear reasons can be checked from my computer but has issues when checked by the GitHub CI.

* doi.org redirecting towards Cloudflare sites.

## Summary page

The script also produce a very convenient summary page for display on GitHub actions pages, like the one shown below:

![alt text](/posts/automatic-link-checker/summary.png)
