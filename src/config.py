from pathlib import Path
import os

PROJECT_ROOT = Path(__file__).parent.parent  # adjust if config.py isn't at project root


def load_env(env_path=PROJECT_ROOT / ".env"):
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


load_env()

DB_PATH = Path(os.environ.get("DB_PATH", "SIM_USAGE_TESTING.db"))
if not DB_PATH.is_absolute():
    DB_PATH = PROJECT_ROOT / DB_PATH