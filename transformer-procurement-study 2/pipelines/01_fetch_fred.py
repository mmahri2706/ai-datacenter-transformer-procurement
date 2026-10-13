"""Bronze layer: download the transformer producer price index from FRED.

Series: Producer Price Index by Industry, Power, Distribution, and Specialty
Transformer Manufacturing. The series ID below must be confirmed in the week 1
data audit (open https://fred.stlouisfed.org/series/<ID> and check the title).

The raw file is saved untouched, with the download date in the file name.
"""

from datetime import date
from pathlib import Path

import requests

SERIES_ID = "PCU335311335311"  # confirm in week 1 audit
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
