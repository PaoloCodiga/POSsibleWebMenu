#!/usr/bin/env sh
set -eu
python3 -m compileall -q . -x '/(artifacts|\.git)/'
python3 - <<'PY'
import ast, pathlib
for path in pathlib.Path('.').rglob('*.py'):
    if '.git' not in path.parts:
        ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
PY
for file in $(find views data -name '*.xml' 2>/dev/null); do xmllint --noout "$file"; done
! rg -n 'publicWidget|options\.registry|web\.ajax|ajax\.jsonRpc|console\.log|^[[:space:]]*print\(' --glob '!docs/**' --glob '!tests/**' --glob '!scripts/**' .
