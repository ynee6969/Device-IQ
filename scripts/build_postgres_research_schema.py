"""Build an additive PostgreSQL research schema from the standalone SQLite definition.

The generated SQL is opt-in and uses research_ table names. It never changes Phone,
User, or the live catalog tables.
"""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
source = (root / "research" / "schema.sql").read_text(encoding="utf-8")
lines = [line for line in source.splitlines() if not line.startswith("PRAGMA ")]
sql = "\n".join(lines)
tables = re.findall(r"CREATE TABLE (\w+)", sql)
for table in sorted(tables, key=len, reverse=True):
    sql = re.sub(rf"\b{table}\b", f"research_{table}", sql)
sql = re.sub(r"CREATE TABLE (research_\w+)", r"CREATE TABLE IF NOT EXISTS \1", sql)
sql = re.sub(r"CREATE INDEX (\w+)", r"CREATE INDEX IF NOT EXISTS research_\1", sql)
sql = sql.replace(" COLLATE NOCASE", "").replace(" REAL", " DOUBLE PRECISION")
sql = re.sub(r"(REFERENCES research_\w+\([^)]*\))", r"\1 DEFERRABLE INITIALLY DEFERRED", sql)
sql += "\nCREATE UNIQUE INDEX IF NOT EXISTS research_models_casefold_unique\n"
sql += "ON research_device_models(category_id, brand_id, lower(model_name));\n"
header = """-- Additive DeviceIQ research tables for the existing PostgreSQL database.
-- Review before applying. Existing application tables and data are untouched.
-- Run the idempotent importer only after this migration succeeds.

"""
target = root / "research" / "postgres_compatibility.sql"
target.write_text((header + sql).rstrip() + "\n", encoding="utf-8")
print(f"{target}: {len(tables)} tables")
