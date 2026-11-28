import time
from pathlib import Path

from copilot.parsing import parse_html

RAW_DIR = Path("data/raw")
TEXT_DIR = Path("data/text")
MIN_CHARS = 50_000


def main() -> None:
    files = sorted(RAW_DIR.glob("*"))
    if not files:
        raise SystemExit("data/raw is empty. Run scripts/download_filings.py first.")
    TEXT_DIR.mkdir(parents=True, exist_ok=True)

    done = skipped = failed = flagged = 0
    for i, path in enumerate(files, start=1):
        out = TEXT_DIR / f"{path.stem}.txt"
        if out.exists():
            skipped += 1
            continue

        start = time.time()
        try:
            text = parse_html(path)
        except Exception as exc:  # noqa: BLE001 - one bad file must not stop the batch
            failed += 1
            print(f"[{i}/{len(files)}] FAILED {path.name}: {exc}")
            continue

        out.write_text(text, encoding="utf-8")
        done += 1

        flags = []
        if len(text) < MIN_CHARS:
            flags.append("SHORT")
        if "risk factors" not in text.lower():
            flags.append("NO-RISK-FACTORS")
        if "us-gaap:" in text:
            flags.append("XBRL-JUNK")
        if flags:
            flagged += 1

        seconds = time.time() - start
        print(
            f"[{i}/{len(files)}] {path.name} | {len(text):,} chars | {seconds:.0f}s | {' '.join(flags)}"
        )

    print(f"\nParsed: {done} | Skipped: {skipped} | Failed: {failed} | Flagged: {flagged}")


if __name__ == "__main__":
    main()
