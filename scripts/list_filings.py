import json
import time
from pathlib import Path

import requests

from copilot.config import get_settings

COMPANIES = {
    "AAPL": "0000320193",
    "MSFT": "0000789019",
    "AMZN": "0001018724",
    "NVDA": "0001045810",
    "TSLA": "0001318605",
    "JPM": "0000019617",
    "GS": "0000886982",
    "XOM": "0000034088",
    "WMT": "0000104169",
    "GOOGL": "0001652044",
}
FORM = "10-K"
PER_COMPANY = 3
OUT_FILE = Path("data/manifest.json")


def main() -> None:
    user_agent = get_settings().sec_user_agent
    if not user_agent or "example.com" in user_agent:
        raise SystemExit("Set SEC_USER_AGENT in .env to your real name and email.")

    manifest = []
    for ticker, cik in COMPANIES.items():
        url = f"https://data.sec.gov/submissions/CIK{cik}.json"
        response = requests.get(url, headers={"User-Agent": user_agent}, timeout=20)
        response.raise_for_status()
        data = response.json()
        recent = data["filings"]["recent"]

        found = 0
        for form, accession, filed, period, doc in zip(
            recent["form"],
            recent["accessionNumber"],
            recent["filingDate"],
            recent["reportDate"],
            recent["primaryDocument"],
        ):
            if form != FORM:
                continue
            folder = accession.replace("-", "")
            manifest.append(
                {
                    "ticker": ticker,
                    "company": data["name"],
                    "cik": cik,
                    "form": form,
                    "filing_date": filed,
                    "period": period,
                    "accession": accession,
                    "document": doc,
                    "url": f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{folder}/{doc}",
                }
            )
            found += 1
            if found == PER_COMPANY:
                break

        print(f"{ticker:6} {data['name']:30} 10-Ks found: {found}")
        time.sleep(0.2)

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(json.dumps(manifest, indent=2))
    print(f"\nSaved {len(manifest)} filings to {OUT_FILE}")


if __name__ == "__main__":
    main()
