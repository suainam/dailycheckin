import json
import os
from pathlib import Path


def load_config(raw_config: str) -> dict:
    try:
        config = json.loads(raw_config)
    except json.JSONDecodeError as exc:
        raise ValueError("DAILYCHECKIN_CONFIG_JSON must contain valid JSON") from exc
    if not isinstance(config, dict):
        raise ValueError("DAILYCHECKIN_CONFIG_JSON must contain a JSON object")
    return config


def write_config(config: dict, path: Path) -> None:
    path.write_text(json.dumps(config, ensure_ascii=False), encoding="utf-8")
    path.chmod(0o600)


def main() -> None:
    raw_config = os.environ.get("DAILYCHECKIN_CONFIG_JSON")
    if not raw_config:
        raise SystemExit("DAILYCHECKIN_CONFIG_JSON is required")
    write_config(load_config(raw_config), Path("config.json"))
    print("DailyCheckIn configuration materialized.")


if __name__ == "__main__":
    main()
