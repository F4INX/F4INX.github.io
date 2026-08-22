---
title: "Switch to Hugo"
date: 2026-08-22
lastmod: 2026-08-22
categories: [Site, Meta]
url: /posts/switch-to-hugo.html
excerpt: "Following several annoying issues with Jekyll, I decided to switch to Hugo."
---

When I started this website, I decided to use a static site generator because it could run for long periods without maintenance, unlike dynamic websites which are subject to security issues and sometimes need emergency patches. I chose GitHub and Jekyll because it was included.

I was very happy with the result, and at the beginning I found the workflow very convenient.

Then came various inconveniences. First, after any reinstallation, Jekyll stopped working on my computer, and I had to use various workarounds. I remember even using a virtual machine on VirtualBox. I eventually managed to get it working again. This issue now occurs less often because I often work in WSL, where Mistral Vibe works better, but I still had various annoyances, such as the need to run `bundler exec`.

The build time is also painfully slow. Sure, I would not have this issue if `--watch --incremental` worked, but it does not because my documents are on a Windows folder while I work in WSL. I want to keep the documents in Windows to have them backed up like everything else. Someday I will rework my workflow, but that will be for another day.

Enough. I decided to migrate to Hugo.

Thanks to Mistral Vibe, the migration was quite feasible. Not as simple as using a converter script, but quite feasible nonetheless.

What I already have from this migration and what I want:

* Faster local builds. Already achieved, and I am really enjoying it.

* Easier installation on Windows. Not currently tested; I will see how well Mistral Vibe works outside of WSL.

* Faster builds on GitHub. This seems to be already the case, but I have not performed formal benchmarks.
