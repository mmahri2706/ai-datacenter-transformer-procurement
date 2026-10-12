"""Silver layer: clean the raw FRED file into a Parquet table.

Reads the newest FRED CSV in data/bronze/, standardizes column names and types,
drops missing values, and writes data/silver/transformer_ppi.parquet.
"""

from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parent.parent
BRONZE_DIR = ROOT / "data" / "bronze"
SILVER_DIR = ROOT / "data" / "silver"


def newest_bronze_file() -> Path:
    files = sorted(BRONZE_DIR.glob("fred_*.csv"))
    if not files:
        raise FileNotFoundError("No FRED file in data/bronze/. Run 01_fetch_fred.py first.")
    return files[-1]


def main() -> None:
    SILVER_DIR.mkdir(parents=True, exist_ok=True)
    source = newest_bronze_file()
    out_path = SILVER_DIR / "transformer_ppi.parquet"

    con = duckdb.connect()
    con.execute(
        f"""
        COPY (
            SELECT
                CAST(observation_date AS DATE) AS month,
                TRY_CAST(value AS DOUBLE)      AS ppi_index
            FROM read_csv('{source.as_posix()}', header = true,
                          columns = {{'observation_date': 'VARCHAR', 'value': 'VARCHAR'}})
            WHERE TRY_CAST(value AS DOUBLE) IS NOT NULL
            ORDER BY month
        ) TO '{out_path.as_posix()}' (FORMAT PARQUET)
        """
    )
    rows = con.execute(f"SELECT COUNT(*) FROM read_parquet('{out_path.as_posix()}')").fetchone()[0]
    print(f"Wrote {rows:,} rows from {source.name} to {out_path}")


if __name__ == "__main__":
    main()
