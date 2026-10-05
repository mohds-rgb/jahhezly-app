from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    'README.md', 'PROJECT_STATE.md', 'OPEN_QUESTIONS.md', 'ASSUMPTIONS.md',
    'RISK_REGISTER.md', 'SECURITY_RISK_REGISTER.md', 'DELIVERY_MANIFEST.md',
    'SECURITY.md', 'CONTRIBUTING.md', 'LICENSE', '.gitignore', '.env.example',
    'backend/pyproject.toml', 'backend/app/main.py', 'backend/app/models.py',
    'backend/migrations/versions/0001_initial.py',
    'apps/mobile/pubspec.yaml', 'apps/mobile/lib/main.dart',
    'docs/ARCHITECTURE.md', 'docs/API_CONTRACT.md', 'docs/DATA_MODEL.md',
]
SECRET_PATTERNS = [
    re.compile(r'BEGIN (?:RSA|OPENSSH|EC) PRIVATE KEY'),
    re.compile(r'(?i)(aws_secret_access_key|private_key)\s*[:=]\s*[A-Za-z0-9+/=_-]{24,}'),
    re.compile(r'(?i)ghp_[A-Za-z0-9]{30,}'),
]
violations=[]
for rel in REQUIRED:
    if not (ROOT/rel).is_file():
        violations.append(f'Missing required file: {rel}')
for path in ROOT.rglob('*'):
    if not path.is_file() or '.git' in path.parts or '__pycache__' in path.parts or '.pytest_cache' in path.parts:
        continue
    try:
        text=path.read_text(encoding='utf-8', errors='ignore')
    except OSError:
        continue
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            violations.append(f'Possible secret pattern in {path.relative_to(ROOT)}')
if violations:
    print('\n'.join(violations))
    raise SystemExit(1)
print('REPOSITORY_VALIDATION_OK')
