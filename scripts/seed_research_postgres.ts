/** Opt-in, repeatable import into additive research_* tables in the existing PostgreSQL DB. */
import fs from "node:fs";
import path from "node:path";
import { PrismaClient } from "@prisma/client";

const root = path.resolve(__dirname, "..");
const input = path.join(root, "outputs", "deviceiq-inventory-2026-11-24", "deviceiq_inventory.json");
const dataset = JSON.parse(fs.readFileSync(input, "utf8")) as {
  metadata: Record<string, string>;
  tables: Record<string, Array<Record<string, string | number | null>>>;
};
const order = [
  "manufacturers", "brands", "device_categories", "data_sources", "device_models",
  "device_configurations", "device_specifications", "philippines_market_releases",
  "device_source_evidence", "raw_research_claims", "research_queue", "excluded_records",
  "audit_log", "scope_settings",
] as const;
const primaryKeys: Record<(typeof order)[number], string> = {
  manufacturers: "manufacturer_id", brands: "brand_id", device_categories: "category_id",
  data_sources: "source_id", device_models: "device_id", device_configurations: "configuration_id",
  device_specifications: "specification_id", philippines_market_releases: "release_id",
  device_source_evidence: "evidence_id", raw_research_claims: "claim_id",
  research_queue: "queue_id", excluded_records: "exclusion_id", audit_log: "audit_id",
  scope_settings: "setting_key",
};

const counts = Object.fromEntries(order.map(table => [table, dataset.tables[table]?.length ?? 0]));
if (!process.argv.includes("--apply")) {
  console.log(JSON.stringify({ mode: "dry-run", cutoff: dataset.metadata.research_cutoff, counts }, null, 2));
  console.log("Apply research/postgres_compatibility.sql, then run this script with --apply to import into research_* tables.");
  process.exit(0);
}
if (!process.env.DATABASE_URL) throw new Error("DATABASE_URL is required for --apply");

async function main() {
const prisma = new PrismaClient();
try {
  await prisma.$transaction(async tx => {
    await tx.$executeRawUnsafe("SET CONSTRAINTS ALL DEFERRED");
    for (const table of order) {
      const rows = dataset.tables[table] ?? [];
      if (!rows.length) continue;
      const columns = Object.keys(rows[0]);
      const key = primaryKeys[table];
      const updates = columns.filter(column => column !== key)
        .map(column => `${column}=EXCLUDED.${column}`).join(",");
      for (let start=0; start<rows.length; start+=40) {
        const batch = rows.slice(start, start+40);
        const parameters = batch.flatMap(row => columns.map(column => row[column] ?? null));
        let index = 0;
        const tuples = batch.map(() => `(${columns.map(() => `$${++index}`).join(",")})`).join(",");
        const sql = `INSERT INTO research_${table} (${columns.join(",")}) VALUES ${tuples} ON CONFLICT (${key}) DO UPDATE SET ${updates}`;
        await tx.$executeRawUnsafe(sql, ...parameters);
      }
    }
  }, { maxWait: 30_000, timeout: 300_000 });
  console.log(JSON.stringify({ mode: "applied", cutoff: dataset.metadata.research_cutoff, counts }, null, 2));
} finally {
  await prisma.$disconnect();
}
}

main().catch(error => { console.error(error); process.exitCode = 1; });
