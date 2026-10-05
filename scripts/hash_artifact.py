from __future__ import annotations
import hashlib
import sys
from pathlib import Path

if len(sys.argv) != 2:
    raise SystemExit('Usage: python scripts/hash_artifact.py <file>')
path = Path(sys.argv[1])
h = hashlib.sha256()
with path.open('rb') as f:
    for chunk in iter(lambda: f.read(1024 * 1024), b''):
        h.update(chunk)
print(f'{h.hexdigest()}  {path}')
