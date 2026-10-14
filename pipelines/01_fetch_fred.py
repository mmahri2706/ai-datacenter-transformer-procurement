"""Bronze layer: download the transformer producer price index from FRED.

Series: Producer Price Index by Industry: Electric Power and Specialty Transformer
Manufacturing (monthly, not seasonally adjusted, index Jun 1981 = 100).
Week 1 audit: the series page was opened and the title and ID matched; the CSV
download itself still needs to be tested on your own computer.

The raw file is saved untouched, with the download date in the file name.
"""

from datetime import date
from pathlib import Path

import requests

SERIES_ID = "PCU335311335311"  # verified against the FRED series page in week 1
URL = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={SERIES_ID}"
BRONZE_DIR = Path(__file__).resolve().parent.parent / "data" / "bronze"


def main() -> None:
    BRONZE_DIR.mkdir(parents=True, exist_ok=True)
    response = requests.get(URL, timeout=60)
    response.raise_for_status()

    out_path = BRONZE_DIR / f"fred_{SERIES_ID}_{date.today().isoformat()}.csv"
    out_path.write_bytes(response.content)
    print(f"Saved {len(response.content):,} bytes to {out_path}")


if __name__ == "__main__":
    main()
