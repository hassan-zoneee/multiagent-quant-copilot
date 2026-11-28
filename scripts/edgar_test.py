import requests

from copilot.config import get_settings

CIK = "0000320193"  # Apple, used as a known example
URL = f"https://data.sec.gov/submissions/CIK{CIK}.json"

user_agent = get_settings().sec_user_agent
if not user_agent or "example.com" in user_agent:
    raise SystemExit("Set SEC_USER_AGENT in .env to your real name and email.")

response = requests.get(URL, headers={"User-Agent": user_agent}, timeout=10)
print("Status:", response.status_code)
response.raise_for_status()

data = response.json()
print("Company:", data["name"])
print("Tickers:", data["tickers"])

recent = data["filings"]["recent"]
print("Fields:", list(recent.keys()))
for form, date, accession in zip(
    recent["form"][:5], recent["filingDate"][:5], recent["accessionNumber"][:5]
):
    print(form, date, accession)
