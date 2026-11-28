import sys
from pathlib import Path

from copilot.parsing import parse_html

path = Path(sys.argv[1]) if len(sys.argv) > 1 else min(Path("data/raw").glob("*"))
text = parse_html(path)

out = Path("data/text") / f"{path.stem}.txt"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(text, encoding="utf-8")

print("File:", path.name)
print("Characters:", len(text), "| Lines:", text.count("\n"))
print("Mentions of 'Risk Factors':", text.count("Risk Factors"))
print("Leftover 'us-gaap:' tags:", text.count("us-gaap:"))
print("--- sample ---")
print(text[5000:5800])
