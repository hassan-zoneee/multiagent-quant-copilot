import re
from pathlib import Path

from bs4 import BeautifulSoup

BLOCK_TAGS = ["p", "div", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6"]


def parse_html(path: Path) -> str:
    soup = BeautifulSoup(path.read_bytes(), "lxml")

    for tag in soup(["script", "style", "ix:header"]):
        tag.extract()

    for tag in soup.find_all(style=re.compile(r"display:\s*none", re.IGNORECASE)):
        tag.extract()

    for table in soup.find_all("table"):
        rows = []
        for tr in table.find_all("tr"):
            cells = [c.get_text(" ", strip=True) for c in tr.find_all(["td", "th"])]
            cells = [c for c in cells if c]
            if cells:
                rows.append(" | ".join(cells))
        table.replace_with(soup.new_string("\n" + "\n".join(rows) + "\n"))

    for br in soup.find_all("br"):
        br.replace_with("\n")
    for tag in soup.find_all(BLOCK_TAGS):
        tag.append("\n")

    text = soup.get_text()
    text = text.replace("\xa0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" ?\n ?", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()
