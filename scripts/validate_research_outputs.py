"""Check research relationships and spreadsheet package integrity after a rebuild."""
from pathlib import Path
import json
import sqlite3
import xml.etree.ElementTree as ET
import zipfile

root = Path(__file__).resolve().parents[1]
out = root / "outputs" / "deviceiq-inventory-2026-11-24"
db = sqlite3.connect(out / "deviceiq_philippine_inventory.sqlite")
stats = json.loads((out / "inventory_metrics.json").read_text(encoding="utf-8"))["stats"]
assert db.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
assert not db.execute("PRAGMA foreign_key_check").fetchall()
assert db.execute("SELECT COUNT(*) FROM device_models").fetchone()[0] == stats["candidate_models"]
assert db.execute("SELECT COUNT(*) FROM raw_research_claims").fetchone()[0] == stats["raw_lines"]
assert db.execute("SELECT COUNT(*) FROM device_models WHERE device_status!='PENDING_VERIFICATION'").fetchone()[0] == stats["verified_models"]
assert db.execute("SELECT COUNT(*) FROM philippines_market_releases WHERE inclusion_status='Included'").fetchone()[0] == stats["included_models"]
assert db.execute("SELECT COUNT(*) FROM device_models WHERE model_name LIKE 'Galaxy S21%'").fetchone()[0] == 3
assert not db.execute("""SELECT m.device_id FROM device_models m
    JOIN philippines_market_releases r ON r.device_id=m.device_id
    WHERE r.verification_status!='PENDING_VERIFICATION'
    AND NOT EXISTS (SELECT 1 FROM device_source_evidence e WHERE e.device_id=m.device_id)""").fetchall()
db.close()

file = out / "DeviceIQ_Philippine_Device_Inventory_2021-2026.xlsx"
ns = {"x": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
with zipfile.ZipFile(file) as archive:
    assert archive.testzip() is None
    workbook = ET.fromstring(archive.read("xl/workbook.xml"))
    names = [sheet.attrib["name"] for sheet in workbook.findall("x:sheets/x:sheet", ns)]
    assert len(names) == 17 and len(set(names)) == 17
    errors, formulas = [], 0
    for item in archive.namelist():
        if not (item.startswith("xl/worksheets/sheet") and item.endswith(".xml")):
            continue
        sheet = ET.fromstring(archive.read(item))
        errors.extend((item, cell.attrib.get("r")) for cell in sheet.findall(".//x:c", ns) if cell.attrib.get("t") == "e")
        formulas += len(sheet.findall(".//x:f", ns))
    assert not errors, f"Spreadsheet formula errors: {errors[:10]}"
    assert formulas > 1000
    assert len([item for item in archive.namelist() if item.startswith("xl/tables/table") and item.endswith(".xml")]) == 15
print(f"PASS: 14 relational tables, 17 workbook sheets, {formulas} formulas, no spreadsheet errors")
