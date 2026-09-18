#!/usr/bin/env python3
"""Check skill metadata, local links, examples and required-reference isolation."""
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def validate(root=ROOT):
    errors = []
    skills = sorted((root / "skills").glob("*/SKILL.md"))
    if not skills:
        errors.append("No skills found")
    for file in skills:
        folder = file.parent
        text = file.read_text(encoding="utf-8")
        match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
        if not match:
            errors.append(f"{file.relative_to(root)}: missing YAML frontmatter")
            continue
        try:
            meta = yaml.safe_load(match[1])
            if not isinstance(meta, dict):
                raise ValueError("frontmatter must be a mapping")
            name, description = meta.get("name"), meta.get("description")
            if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
                raise ValueError("invalid skill name")
            if name != folder.name:
                raise ValueError("name must match directory")
            if not isinstance(description, str) or not 1 <= len(description.strip()) <= 1024:
                raise ValueError("description must contain 1–1024 characters")
            if len(text.splitlines()) >= 500:
                raise ValueError("move detail from SKILL.md into references; entry point is 500+ lines")
            if re.search(r"\[TODO:|TODO: replace|TBD", text):
                raise ValueError("unfinished scaffold")
            ui = yaml.safe_load((folder / "agents/openai.yaml").read_text(encoding="utf-8"))
            interface = ui["interface"]
            if not isinstance(interface.get("display_name"), str) or not interface["display_name"].strip():
                raise ValueError("missing display_name")
            short = interface.get("short_description", "")
            if not isinstance(short, str) or not 25 <= len(short) <= 64:
                raise ValueError("short_description must contain 25–64 characters")
            if f"${name}" not in interface.get("default_prompt", ""):
                raise ValueError("default_prompt must name the skill")
            if ui.get("policy", {}).get("allow_implicit_invocation", True) is not True:
                raise ValueError("implicit invocation unexpectedly disabled")
        except (ValueError, TypeError, KeyError, OSError, yaml.YAMLError) as exc:
            errors.append(f"{folder.relative_to(root)}: {exc}")
        for required in ("README.md", "references/sources.md"):
            if not (folder / required).is_file():
                errors.append(f"{folder.relative_to(root)}: missing {required}")
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
            if re.match(r"[a-z]+:", target) or target.startswith("#"):
                continue
            dest = (folder / target.split("#", 1)[0]).resolve()
            if not dest.is_relative_to(folder.resolve()):
                errors.append(f"{folder.name}: SKILL requires a link outside its standalone folder: {target}")
    for file in root.rglob("*.md"):
        if ".git" in file.parts:
            continue
        for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", file.read_text(encoding="utf-8")):
            if re.match(r"[a-z]+:", target) or target.startswith("#"):
                continue
            path = target.split("#", 1)[0]
            if path and not (file.parent / path).exists():
                errors.append(f"{file.relative_to(root)}: broken local link {target}")
    for file in (root / "skills").glob("*/examples/*.json"):
        try:
            data = json.loads(file.read_text(encoding="utf-8"))
            if not data.get("_example_notice"):
                errors.append(f"{file.relative_to(root)}: synthetic example notice is required")
        except (ValueError, OSError) as exc:
            errors.append(f"{file.relative_to(root)}: {exc}")
    return skills, errors


if __name__ == "__main__":
    skills, errors = validate()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        sys.exit(1)
    print(f"Validated {len(skills)} skill folders, UI metadata, local links and JSON examples.")
