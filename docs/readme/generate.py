#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "Jinja2>=3.1,<4",
#   "PyYAML>=6,<7",
# ]
# ///
"""Generate and verify the localized root README files.

Run from the repository root:
    uv run docs/readme/generate.py
    uv run docs/readme/generate.py --check
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined


README_DIR = Path(__file__).resolve().parent
REPOSITORY_DIR = README_DIR.parents[1]


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as file:
        document = yaml.safe_load(file)
    if not isinstance(document, dict):
        raise ValueError(f"{path.relative_to(REPOSITORY_DIR)} must contain a mapping")
    return document


def compare_keys(reference: Any, candidate: Any, path: str = "") -> list[str]:
    if isinstance(reference, dict):
        if not isinstance(candidate, dict):
            return [f"{path} must be a mapping"]
        errors: list[str] = []
        reference_keys = set(reference)
        candidate_keys = set(candidate)
        for key in sorted(reference_keys - candidate_keys):
            errors.append(f"missing key: {path}{key}")
        for key in sorted(candidate_keys - reference_keys):
            errors.append(f"unexpected key: {path}{key}")
        for key in sorted(reference_keys & candidate_keys):
            errors.extend(compare_keys(reference[key], candidate[key], f"{path}{key}."))
        return errors
    if isinstance(reference, list):
        if not isinstance(candidate, list):
            return [f"{path[:-1]} must be a list"]
        if len(reference) != len(candidate):
            return [f"{path[:-1]} must contain {len(reference)} entries, found {len(candidate)}"]
        errors = []
        for index, (reference_item, candidate_item) in enumerate(zip(reference, candidate, strict=True)):
            errors.extend(compare_keys(reference_item, candidate_item, f"{path}{index}."))
        return errors
    if not isinstance(candidate, str):
        return [f"{path[:-1]} must be a string"]
    return []


def render(template_name: str, translations: dict[str, Any], locales: list[dict[str, str]], code: str) -> str:
    environment = Environment(
        loader=FileSystemLoader(README_DIR),
        undefined=StrictUndefined,
        keep_trailing_newline=True,
        trim_blocks=False,
        lstrip_blocks=False,
    )
    template = environment.get_template(template_name)
    return template.render(t=translations, locales=locales, code=code).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate localized root README files")
    parser.add_argument("--check", action="store_true", help="fail when generated files are stale")
    arguments = parser.parse_args()

    config = load_yaml(README_DIR / "config.yml")
    locales = config.get("locales")
    if not isinstance(locales, list) or not locales:
        raise ValueError("docs/readme/config.yml must define at least one locale")
    if any(not isinstance(locale, dict) for locale in locales):
        raise ValueError("every locale in docs/readme/config.yml must be a mapping")

    required_locale_keys = {"code", "name", "source", "output"}
    for locale in locales:
        if set(locale) != required_locale_keys or not all(isinstance(value, str) for value in locale.values()):
            raise ValueError("every locale must contain string code, name, source, and output values")

    source_files = [locale["source"] for locale in locales]
    output_files = [locale["output"] for locale in locales]
    if len(source_files) != len(set(source_files)) or len(output_files) != len(set(output_files)):
        raise ValueError("locale source and output paths must each be unique")

    locale_data = {locale["code"]: load_yaml(README_DIR / locale["source"]) for locale in locales}
    reference = locale_data["en"]
    validation_errors: list[str] = []
    for locale in locales:
        code = locale["code"]
        if code == "en":
            continue
        validation_errors.extend(f"{code}: {error}" for error in compare_keys(reference, locale_data[code]))
    if validation_errors:
        raise ValueError("language package keys do not match English:\n  " + "\n  ".join(validation_errors))

    stale_files: list[Path] = []
    for locale in locales:
        output_path = REPOSITORY_DIR / locale["output"]
        generated = render("README.md.j2", locale_data[locale["code"]], locales, locale["code"])
        if arguments.check:
            if not output_path.is_file() or output_path.read_text(encoding="utf-8") != generated:
                stale_files.append(output_path)
        else:
            output_path.write_text(generated, encoding="utf-8", newline="\n")

    if stale_files:
        print("Generated README files are stale:", file=sys.stderr)
        for path in stale_files:
            print(f"  {path.relative_to(REPOSITORY_DIR)}", file=sys.stderr)
        print("Run: uv run docs/readme/generate.py", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, yaml.YAMLError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1) from error
