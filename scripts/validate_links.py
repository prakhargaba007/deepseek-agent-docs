#!/usr/bin/env python3
"""
validate_links.py — Check all HTTP/HTTPS links in deepseek.md for broken URLs.

Usage:
    python scripts/validate_links.py
    python scripts/validate_links.py --file deepseek.md --timeout 10

Requires: pip install requests
"""

import argparse
import re
import sys
import time
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    print("Error: 'requests' package not found. Run: pip install requests")
    sys.exit(1)


# ── Configuration ─────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).parent.parent
DEFAULT_FILE = REPO_ROOT / "deepseek.md"

# Domains to skip (known to block bots, or require auth)
SKIP_DOMAINS = {
    "platform.deepseek.com",  # Requires login
    "trtgsjkv6r.feishu.cn",   # May require auth
    "cdn.deepseek.com",       # File downloads — skip
}

# Regex to extract markdown links: [text](url) and bare URLs
LINK_PATTERNS = [
    re.compile(r'\]\((https?://[^\s\)]+)\)'),   # [text](url)
    re.compile(r'(?<!\()https?://[^\s\)>\]\n]+'),  # bare URLs in text
]


# ── Core logic ────────────────────────────────────────────────────────────────

def extract_links(text: str) -> list[tuple[int, str]]:
    """Extract all HTTP/HTTPS links with their line numbers."""
    links = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for pattern in LINK_PATTERNS:
            for match in pattern.finditer(line):
                url = match.group(1) if match.lastindex else match.group(0)
                url = url.rstrip(".,;)")  # Strip trailing punctuation
                links.append((lineno, url))
    return links


def check_link(
    url: str,
    timeout: int = 10,
    session: Optional[requests.Session] = None,
) -> tuple[bool, int, str]:
    """Check if a URL is reachable. Returns (ok, status_code, error_msg)."""
    parsed = urlparse(url)
    if parsed.netloc in SKIP_DOMAINS:
        return True, 0, "skipped"

    sess = session or requests.Session()
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (compatible; deepseek-docs-link-checker/1.0; "
            "+https://github.com/prakhargaba007/deepseek-agent-docs)"
        )
    }

    try:
        response = sess.head(url, headers=headers, timeout=timeout, allow_redirects=True)
        if response.status_code == 405:
            # HEAD not allowed — try GET
            response = sess.get(url, headers=headers, timeout=timeout, allow_redirects=True, stream=True)
        ok = response.status_code < 400
        return ok, response.status_code, ""
    except requests.exceptions.ConnectionError as e:
        return False, 0, f"Connection error: {e}"
    except requests.exceptions.Timeout:
        return False, 0, f"Timed out after {timeout}s"
    except Exception as e:
        return False, 0, str(e)


def main():
    parser = argparse.ArgumentParser(description="Validate links in a Markdown file.")
    parser.add_argument("--file", default=str(DEFAULT_FILE), help="Path to Markdown file")
    parser.add_argument("--timeout", type=int, default=10, help="HTTP request timeout in seconds")
    parser.add_argument("--delay", type=float, default=0.5, help="Delay between requests (seconds)")
    args = parser.parse_args()

    md_file = Path(args.file)
    if not md_file.exists():
        print(f"Error: File not found: {md_file}")
        sys.exit(1)

    print(f"Checking links in: {md_file}")
    text = md_file.read_text(encoding="utf-8")

    # Deduplicate while preserving first occurrence line number
    seen: dict[str, int] = {}
    for lineno, url in extract_links(text):
        if url not in seen:
            seen[url] = lineno

    total = len(seen)
    print(f"Found {total} unique link(s).\n")

    broken: list[tuple[int, str, int, str]] = []
    session = requests.Session()

    for i, (url, lineno) in enumerate(seen.items(), 1):
        print(f"[{i:3d}/{total}] Line {lineno:4d}: {url[:80]}", end="", flush=True)
        ok, status, error = check_link(url, timeout=args.timeout, session=session)

        if ok:
            label = f"✅ {status}" if status else "⏭️  skipped"
        else:
            label = f"❌ {status or 'ERR'} — {error}"
            broken.append((lineno, url, status, error))

        print(f"  {label}")
        time.sleep(args.delay)

    print(f"\n{'─' * 60}")
    print(f"Results: {total - len(broken)} OK, {len(broken)} broken")

    if broken:
        print("\n🔴 Broken links:\n")
        for lineno, url, status, error in broken:
            print(f"  Line {lineno}: {url}")
            print(f"    → {status or 'ERROR'}: {error}\n")
        sys.exit(1)
    else:
        print("\n✅ All links are valid!")
        sys.exit(0)


if __name__ == "__main__":
    main()
