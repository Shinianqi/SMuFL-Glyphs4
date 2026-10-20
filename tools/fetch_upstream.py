#!/usr/bin/env python3
"""Refresh data/upstream/ from the official SMuFL repository.

    python3 tools/fetch_upstream.py --ref f9d12b22ea89978720ba9defb2f4df67fabd8564

Uses the GitHub contents API (works where raw.githubusercontent.com is
blocked).  Afterwards run `python3 tools/build_all.py` and commit both the
new upstream files and the regenerated output.

The files are the SMuFL specification metadata, published by the W3C Music
Notation Community Group under the W3C Community Final Specification
Agreement.  Nothing is taken from any third-party Glyphs package.
"""
from __future__ import annotations

import argparse
import base64
import datetime
import hashlib
import json
import os
import sys
import urllib.request

import smufl_common as common

REPO = "w3c-cg/smufl"
FILES = ("glyphnames.json", "classes.json", "ranges.json")
API = "https://api.github.com/repos/%s" % REPO


def get_json(url: str) -> dict:
    request = urllib.request.Request(
        url, headers={"Accept": "application/vnd.github+json",
                      "User-Agent": "smufl-glyphs4-build"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def fetch(ref: str) -> None:
    commit = get_json("%s/commits/%s" % (API, ref))
    sha = commit["sha"]
    date = commit["commit"]["committer"]["date"]
    os.makedirs(common.UPSTREAM, exist_ok=True)

    digests = {}
    for name in FILES:
        payload = get_json("%s/contents/metadata/%s?ref=%s" % (API, name, sha))
        data = base64.b64decode(payload["content"])
        path = os.path.join(common.UPSTREAM, name)
        with open(path, "wb") as handle:
            handle.write(data)
        digests[name] = hashlib.sha256(data).hexdigest()
        print("fetched %-16s %8d bytes  %s" % (name, len(data), digests[name]))

    version = {
        "source": "https://github.com/%s" % REPO,
        "branch": "gh-pages",
        "commit": sha,
        "commitDate": date,
        "retrieved": datetime.date.today().isoformat(),
        "specVersion": "1.5 (draft)",
        "files": list(FILES),
    }
    common.write_json(os.path.join(common.UPSTREAM, "VERSION.json"), version)
    common.write_text(
        os.path.join(common.UPSTREAM, "SHA256SUMS"),
        "".join("%s  %s\n" % (digests[name], name) for name in FILES),
    )
    print("pinned commit", sha)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ref", default="gh-pages",
                        help="branch, tag or commit (default: gh-pages HEAD)")
    args = parser.parse_args()
    fetch(args.ref)
    return 0


if __name__ == "__main__":
    sys.exit(main())
