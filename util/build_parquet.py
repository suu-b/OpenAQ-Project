import duckdb

con = duckdb.connect('../db/air_quality_duckdb')

con.execute("""
COPY (
    SELECT *
    FROM read_csv_auto('../data/raw/**/*.csv.gz')
) TO '../data/parquet/all_data.parquet' (FORMAT parquet)
""")