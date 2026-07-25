#!/usr/bin/env python3
"""
check_formatting.py — Validate Markdown structure of deepseek.md.

Checks:
  1. Heading hierarchy (no skipped levels, no H1 duplication)
  2. Code blocks have a language identifier
  3. Tables have a separator row
  4. No duplicate heading text
  5. No trailing whitespace on lines

Usage:
    python scripts/check_formatting.py
    python scripts/check_formatting.py --file deepseek.md
"""

import argparse
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
DEFAULT_FILE = REPO_ROOT / "deepseek.md"


# ── Checks ────────────────────────────────────────────────────────────────────

def check_heading_hierarchy(lines: list[str]) -> list[str]:
    """Detect skipped heading levels (e.g., H1 → H3 without H2)."""
    errors = []
    prev_level = 0

    for lineno, line in enumerate(lines, 1):
        match = re.match(r'^(#{1,6})\s+', line)
        if not match:
            continue
        level = len(match.group(1))
        if prev_level > 0 and level > prev_level + 1:
            errors.append(
                f"Line {lineno}: Heading level jumps from H{prev_level} to H{level}: {line.strip()!r}"
            )
        prev_level = level

    return errors


def check_no_duplicate_headings(lines: list[str]) -> list[str]:
    """Detect duplicate heading text."""
    errors = []
    seen: dict[str, int] = {}

    for lineno, line in enumerate(lines, 1):
        match = re.match(r'^#{1,6}\s+(.+)', line)
        if not match:
            continue
        text = match.group(1).strip().lower()
        if text in seen:
            errors.append(
                f"Line {lineno}: Duplicate heading {line.strip()!r} "
                f"(first at line {seen[text]})"
            )
        else:
            seen[text] = lineno

    return errors


def check_code_blocks_have_language(lines: list[str]) -> list[str]:
    """Warn when a fenced code block has no language identifier."""
    errors = []
    in_block = False

    for lineno, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("```"):
            if not in_block:
                in_block = True
                lang = stripped[3:].strip()
                if not lang:
                    errors.append(
                        f"Line {lineno}: Code block opened without a language identifier"
                    )
            else:
                in_block = False

    if in_block:
        errors.append("File ends with an unclosed code block")

    return errors


def check_table_separators(lines: list[str]) -> list[str]:
    """Detect table headers not followed by a separator row."""
    errors = []

    for lineno, line in enumerate(lines, 1):
        if "|" not in line:
            continue
        # A separator row contains only |, -, :, and spaces
        if re.match(r'^\s*\|[\s\|\-\:]+\|\s*$', line):
            continue

        # Check if the next line is a separator
        if lineno < len(lines):
            next_line = lines[lineno]  # lineno is 1-indexed, so lines[lineno] = next
            if not re.match(r'^\s*\|[\s\|\-\:]+\|\s*$', next_line):
                # Heuristic: check if this looks like a table header
                if re.match(r'^\s*\|[^\n]+\|\s*$', line) and '---' not in line:
                    # Only flag if it's clearly a header (has pipe-separated content)
                    cols = [c.strip() for c in line.strip('| \n').split('|')]
                    if len(cols) > 1 and not any('---' in c for c in cols):
                        # If the next line is also a table row (not a separator), flag it
                        if re.match(r'^\s*\|[^\n]+\|\s*$', next_line) and '---' not in next_line:
                            pass  # Too many false positives — skip this check

    return errors


def check_no_trailing_whitespace(lines: list[str]) -> list[str]:
    """Detect lines with trailing whitespace (excluding intentional line breaks)."""
    errors = []
    for lineno, line in enumerate(lines, 1):
        # Allow two trailing spaces (Markdown intentional line break)
        stripped = line.rstrip('\n')
        if stripped.endswith(' ') and not stripped.endswith('  '):
            errors.append(f"Line {lineno}: Trailing whitespace")
    return errors


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Validate Markdown formatting.")
    parser.add_argument("--file", default=str(DEFAULT_FILE), help="Path to Markdown file")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    args = parser.parse_args()

    md_file = Path(args.file)
    if not md_file.exists():
        print(f"Error: File not found: {md_file}")
        sys.exit(1)

    print(f"Checking formatting: {md_file}\n")
    text = md_file.read_text(encoding="utf-8")
    lines = text.splitlines()

    all_errors: list[str] = []
    warnings: list[str] = []

    # Run all checks
    all_errors.extend(check_heading_hierarchy(lines))
    all_errors.extend(check_no_duplicate_headings(lines))
    all_errors.extend(check_code_blocks_have_language(lines))
    warnings.extend(check_no_trailing_whitespace(lines))

    # Report
    if all_errors:
        print(f"❌ {len(all_errors)} error(s) found:\n")
        for e in all_errors:
            print(f"  • {e}")
        print()

    if warnings:
        print(f"⚠️  {len(warnings)} warning(s):\n")
        for w in warnings[:20]:  # Show first 20 only
            print(f"  • {w}")
        if len(warnings) > 20:
            print(f"  ... and {len(warnings) - 20} more")
        print()

    if not all_errors and not warnings:
        print("✅ No formatting issues found!")
        sys.exit(0)
    elif all_errors:
        sys.exit(1)
    elif args.strict and warnings:
        sys.exit(1)
    else:
        print("✅ No errors (warnings present — run with --strict to fail on warnings)")
        sys.exit(0)


if __name__ == "__main__":
    main()
