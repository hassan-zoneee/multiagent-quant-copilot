import json
import time
from pathlib import Path

import requests

from copilot.config import get_settings

MANIFEST = Path("data/manifest.json")
RAW_DIR = Path("data/raw")


def main():
    user_agent = get_settings().sec_user_agent
    if not user_agent or "example.com" in user_agent:
        raise SystemExit("Set Sec_User_Agent in .env")
    if not MANIFEST.exists():
        raise SystemExit("Run scripts/list_filings.py first")

    filings = json.loads(MANIFEST.read_text())
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    downloaded = skipped = failed = 0

    for i, f in enumerate(filings, start=1):
        suffix = Path(f["document"]).suffix or ".htm"
        target = RAW_DIR / f"{f['ticker']}_{f['period']}_{f['accession']}{suffix}"

        if target.exists():
            skipped += 1
            continue

        try:
            response = requests.get(f["url"], headers={"User-Agent": user_agent}, timeout=60)
            response.raise_for_status()
        except Exception as exce:  # noqa: BLE001
            failed += 1
            print(f"[{i}/{len(filings)}] FAILED {f['ticker']} {f['period']}: {exce}")
            time.sleep(1)
            continue

        target.write_bytes(response.content)
        downloaded += 1
        size_mb = len(response.content) / 1_000_000
        print(f"[{i}/{len(filings)}] {target.name} ({size_mb:.1f} MB)")
        time.sleep(0.3)

    print(f"\nDownloaded: {downloaded} | Skipped (already had): {skipped} | Failed: {failed}")


if __name__ == "__main__":
    main()
