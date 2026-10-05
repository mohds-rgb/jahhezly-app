from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "apps" / "mobile"
errors: list[str] = []

dart_files = list((ROOT / "lib").rglob("*.dart")) + list((ROOT / "test").rglob("*.dart"))
for path in dart_files:
    text = path.read_text(encoding="utf-8")
    for raw in re.findall(r"(?:import|export)\s+'(\.\.?/[^']+)'", text):
        target = (path.parent / raw).resolve()
        if not target.exists():
            errors.append(f"Broken Dart relative import: {path.relative_to(ROOT)} -> {raw}")

pubspec = (ROOT / "pubspec.yaml").read_text(encoding="utf-8")
for asset in re.findall(r"\-\s+([^\s#]+)", pubspec):
    if asset.startswith("assets/") and not (ROOT / asset).exists():
        errors.append(f"Missing declared asset: {asset}")

if errors:
    print("\n".join(errors))
    raise SystemExit(1)
print(f"MOBILE_STRUCTURE_OK dart_files={len(dart_files)}")
