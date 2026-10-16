"""Generate MkDocs navigation from monthly forecast files."""

from pathlib import Path
import calendar
import re
import yaml

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "src"
CONFIG = ROOT / "mkdocs.yml"
OUTPUT = ROOT / "mkdocs.generated.yml"

# Load existing configuration
with CONFIG.open(encoding="utf-8") as f:
    config = yaml.safe_load(f)

# Static navigation
nav = [
    {"XRO Wave Model": "index.md"},
    {"Disclaimer": "disclaimer.md"},
    {"References": "references.md"},
]

# Automatically discover forecast years and months
for year_dir in sorted(SOURCE.iterdir(), reverse=True):
    if not year_dir.is_dir() or not re.fullmatch(r"\d{4}", year_dir.name):
        continue

    months = []

    for month in range(12, 0, -1):
        month_name = calendar.month_name[month]
        file = year_dir / f"{month_name.lower()}.md"

        if file.is_file():
            months.append({
                month_name: f"{year_dir.name}/{file.name}"
            })

    if months:
        nav.append({
            f"Forecasts {year_dir.name}": months
        })

config["nav"] = nav

# Save generated configuration
with OUTPUT.open("w", encoding="utf-8") as f:
    yaml.safe_dump(
        config,
        f,
        sort_keys=False,
        allow_unicode=True,
    )

print(f"Generated: {OUTPUT}")
for item in nav:
    print(item)


