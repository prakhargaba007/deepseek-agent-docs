# Maintenance Scripts

Python utility scripts for maintainers to validate and maintain `deepseek.md`.

## Requirements

```bash
pip install requests
```

## Scripts

### `validate_links.py`

Checks all HTTP/HTTPS links found in `deepseek.md` and reports broken ones.

```bash
python scripts/validate_links.py
python scripts/validate_links.py --file deepseek.md --timeout 10
```

### `check_formatting.py`

Validates the Markdown structure of `deepseek.md`:
- Heading hierarchy (no skipped levels)
- Code blocks have language identifiers
- Tables have proper separators
- No duplicate headings

```bash
python scripts/check_formatting.py
python scripts/check_formatting.py --file deepseek.md
```

### `generate_toc.py`

Generates or updates the Table of Contents in `deepseek.md` based on
its current heading structure.

```bash
# Print the generated ToC to stdout
python scripts/generate_toc.py

# Write directly to a file (dry-run by default)
python scripts/generate_toc.py --write
```
