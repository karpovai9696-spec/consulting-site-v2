# Синхронизация сайта с админкой
#
# Забирает публичный JSON сайта consulting из админки,
# сохраняет его в data/admin-export.json и пересобирает HTML.
#
# Запуск:
#   ADMIN_PUBLIC_URL=https://127.0.0.1:18090/api/public/sites/consulting.json python scripts/sync_admin.py

import json
import os
import ssl
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADMIN_URL = os.environ.get(
    "ADMIN_PUBLIC_URL",
    "https://127.0.0.1:18090/api/public/sites/consulting.json",
)

ctx = ssl._create_unverified_context()
req = urllib.request.Request(ADMIN_URL, headers={"Accept": "application/json"})
try:
    with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
        data = json.loads(resp.read().decode("utf-8"))
except Exception as exc:
    print(f"Не удалось получить JSON из админки: {exc}", file=sys.stderr)
    sys.exit(1)

if data.get("site", {}).get("slug") != "consulting":
    print("В ответе не сайт consulting", file=sys.stderr)
    sys.exit(1)

(ROOT / "data").mkdir(exist_ok=True)
(ROOT / "data" / "admin-export.json").write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
print("Экспорт сохранён:", data.get("exported_at"))

subprocess.run(
    [sys.executable, str(ROOT / "scripts" / "build_site.py")],
    check=True,
    cwd=str(ROOT),
)
print("Сайт пересобран.")
