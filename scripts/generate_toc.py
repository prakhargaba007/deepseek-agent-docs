#!/usr/bin/env python3
"""
generate_toc.py — Generate or update the Table of Contents in deepseek.md.

Reads all headings from the file and generates a Markdown ToC with proper
anchor links (GitHub-compatible slug format).

Usage:
    # Print generated ToC to stdout
    python scripts/generate_toc.py

    # Write ToC back to the file (replaces existing ToC section)
    python scripts/generate_toc.py --write

    # Target a different file
    python scripts/generate_toc.py --file docs/api.md
"""

import argparse
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
DEFAULT_FILE = REPO_ROOT / "deepseek.md"

# Markers for the ToC section in the file
TOC_START_MARKER = "## Table of Contents"
TOC_END_MARKER = "\n---\n"


# ── Heading → Anchor slug (GitHub-compatible) ─────────────────────────────────

def heading_to_anchor(text: str) -> str:
    """Convert a heading to a GitHub Markdown anchor slug."""
    slug = text.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)   # Remove special chars (keep alphanumeric, space, dash)
    slug = re.sub(r'[\s]+', '-', slug)     # Spaces → dashes
    slug = slug.strip('-')
    return slug


# ── ToC generation ────────────────────────────────────────────────────────────

def generate_toc(lines: list[str], min_level: int = 2, max_level: int = 4) -> str:
    """Generate a Markdown ToC from a list of lines."""
    toc_lines = []
    in_code_block = False

    for line in lines:
        # Track code blocks to skip headings inside them
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        match = re.match(r'^(#{1,6})\s+(.+)', line)
        if not match:
            continue

        level = len(match.group(1))
        if level < min_level or level > max_level:
            continue

        text = match.group(2).strip()
        # Remove inline code from anchor text (but keep it in display)
        anchor_text = re.sub(r'`[^`]+`', lambda m: m.group(0)[1:-1], text)
        anchor = heading_to_anchor(anchor_text)

        indent = "  " * (level - min_level)
        toc_lines.append(f"{indent}- [{text}](#{anchor})")

    return "\n".join(toc_lines)


# ── File update ───────────────────────────────────────────────────────────────

def update_file_toc(file_path: Path, new_toc: str) -> bool:
    """Replace the existing ToC section in the file. Returns True if changed."""
    content = file_path.read_text(encoding="utf-8")

    # Find the ToC section
    toc_start = content.find(TOC_START_MARKER)
    if toc_start == -1:
        print(f"Warning: Could not find ToC marker {TOC_START_MARKER!r} in file.")
        return False

    # Find the end of the ToC (first --- after the ToC section)
    toc_content_start = toc_start + len(TOC_START_MARKER) + 1
    toc_end = content.find(TOC_END_MARKER, toc_content_start)

    if toc_end == -1:
        print("Warning: Could not find ToC end marker. ToC section not updated.")
        return False

    # Replace the ToC section
    new_toc_section = f"{TOC_START_MARKER}\n\n{new_toc}\n"
    new_content = content[:toc_start] + new_toc_section + content[toc_end:]

    if new_content == content:
        return False  # No change

    file_path.write_text(new_content, encoding="utf-8")
    return True


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate Table of Contents for a Markdown file.")
    parser.add_argument("--file", default=str(DEFAULT_FILE), help="Path to Markdown file")
    parser.add_argument("--write", action="store_true", help="Write ToC back to the file")
    parser.add_argument("--min-level", type=int, default=2, help="Minimum heading level to include (default: 2)")
    parser.add_argument("--max-level", type=int, default=4, help="Maximum heading level to include (default: 4)")
    args = parser.parse_args()

    md_file = Path(args.file)
    if not md_file.exists():
        print(f"Error: File not found: {md_file}")
        sys.exit(1)

    text = md_file.read_text(encoding="utf-8")
    lines = text.splitlines()

    toc = generate_toc(lines, min_level=args.min_level, max_level=args.max_level)

    if args.write:
        changed = update_file_toc(md_file, toc)
        if changed:
            print(f"✅ Table of Contents updated in {md_file}")
        else:
            print(f"ℹ️  Table of Contents is already up to date.")
    else:
        print("## Table of Contents\n")
        print(toc)
        print(f"\n[{toc.count(chr(10)) + 1} entries | Run with --write to update the file]")


if __name__ == "__main__":
    main()
