import assert from "node:assert/strict";
import { CATALOG_VERSION, catalogDevices, catalogRows } from "../lib/catalog/data";
import { fieldOptions, filterDefinitions, filterRows, pageRows, sortRows, type FilterSelections } from "../lib/catalog/filtering";
import type { CatalogRow, DeviceCategory } from "../lib/catalog/types";
import packageJson from "../package.json";

const testedAt = "2026-11-23";
const cases: { id: string; category: DeviceCategory; filters: FilterSelections; expected: string[]; note: string }[] = [
  { id: "T01", category: "tablets", filters: { "chipset:multi": ["Snapdragon 7s Gen 4"] }, expected: ["poco-pad-m1", "redmi-pad-2-pro"], note: "Exact chipset" },
  { id: "T02", category: "tablets", filters: { "ramGb:min": 8 }, expected: ["poco-pad-m1", "poco-pad-x1", "redmi-pad-2-pro", "samsung-tab-s10-fe", "xiaomi-pad-7", "xiaomi-pad-7-pro", "xiaomi-pad-8", "xiaomi-pad-8-pro", "xiaomi-pad-mini"], note: "Inclusive RAM threshold" },
  { id: "T03", category: "tablets", filters: { "brand:multi": ["POCO", "REDMI"] }, expected: ["poco-pad-m1", "poco-pad-x1", "redmi-pad-2-pro", "redmi-pad-se-87-4g"], note: "OR within brand" },
  { id: "T04", category: "tablets", filters: { "brand:multi": ["POCO"], "batteryMah:min": 10000 }, expected: ["poco-pad-m1"], note: "AND across fields" },
  { id: "T05", category: "tablets", filters: { "pricePhp:max": 30000 }, expected: [], note: "Missing prices fail active price filter" },
  { id: "T06", category: "tablets", filters: { "brand:multi": ["POCO"], "batteryMah:min": 13000 }, expected: [], note: "No match preserves selected filters" },
  { id: "T07", category: "tablets", filters: { "brand:multi": ["POCO"] }, expected: ["poco-pad-m1", "poco-pad-x1"], note: "Relaxed battery filter" },
  { id: "L01", category: "laptops", filters: { "cpu:multi": ["Intel Core Ultra 9 275HX"] }, expected: ["acer-predator-phn16-73", "acer-predator-phn16s-71"], note: "Exact CPU" },
  { id: "L02", category: "laptops", filters: { "ramGb:min": 16, "pricePhp:max": 55000 }, expected: ["acer-aspire-go-ag15-43p", "acer-swift-go-sfg14-01"], note: "Minimum RAM with maximum price" },
  { id: "L03", category: "laptops", filters: { "laptopType:multi": ["Gaming"], "gpu:multi": ["NVIDIA GeForce RTX 5070"] }, expected: ["acer-predator-phn16s-71"], note: "Laptop-specific exact GPU" },
  { id: "L04", category: "laptops", filters: { "priceCondition:multi": ["used"] }, expected: [], note: "No invented used prices" },
  { id: "L05", category: "laptops", filters: { "pricePhp:max": 55000 }, expected: ["acer-aspire-go-ag15-43p", "acer-aspire-lite-al14-42p", "acer-aspire-lite-al15-33p", "acer-swift-go-sfg14-01"], note: "Inclusive price filtering" },
  { id: "S01", category: "smartphones", filters: { "chipset:multi": ["Snapdragon 8 Elite"] }, expected: ["poco-f7-ultra", "xiaomi-15", "xiaomi-15-ultra"], note: "Exact phone chipset" },
  { id: "S02", category: "smartphones", filters: { "ramGb:min": 12 }, expected: ["poco-f7", "poco-f7-pro", "poco-f7-ultra", "xiaomi-15", "xiaomi-15-ultra"], note: "Inclusive phone RAM threshold" },
  { id: "S03", category: "smartphones", filters: { "brand:multi": ["POCO", "Samsung"] }, expected: ["poco-f7", "poco-f7-pro", "poco-f7-ultra", "poco-x7-pro", "samsung-galaxy-a56-5g"], note: "OR within phone brands" },
  { id: "S04", category: "smartphones", filters: { "brand:multi": ["REDMI"], "batteryMah:min": 5500 }, expected: ["redmi-note-14"], note: "AND across phone fields" },
  { id: "S05", category: "smartphones", filters: { "pricePhp:max": 20000 }, expected: [], note: "Unknown phone prices do not pass a price filter" },
  { id: "S06", category: "smartphones", filters: { "brand:multi": ["REDMI"], "batteryMah:min": 7000 }, expected: [], note: "No matching phone" }
];

let passed = 0;
for (const test of cases) {
  const rows = catalogRows(test.category);
  const actual = filterRows(rows, filterDefinitions(test.category), test.filters).map(({ device }) => device.id).sort();
  const expected = [...test.expected].sort();
  assert.deepEqual(actual, expected, `${test.id}: ${test.note}`);
  console.log(JSON.stringify({ id: test.id, category: test.category, dataset: CATALOG_VERSION, softwareVersion: packageJson.version, filters: test.filters, expected, observed: actual, testedAt, status: "pass", note: test.note }));
  passed++;
}

assert.equal(catalogRows("tablets").length, 10);
assert.equal(catalogRows("laptops").length, 10);
assert.equal(catalogRows("smartphones").length, 10);
assert.equal(catalogDevices.length, 30);
assert.ok(catalogDevices.every((device) => device.sources.length > 0 && device.sources.every((source) => source.url.startsWith("https://") && source.observedAt === testedAt)));
assert.ok(catalogDevices.every((device) => device.variants.every((variant) => variant.pricePhp === null || Boolean(variant.priceSourceUrl && variant.priceObservedAt && variant.priceCondition))));
console.log("Catalog counts, source links, and price provenance: pass");
passed++;

const tabletRows = catalogRows("tablets");
assert.ok(!fieldOptions(tabletRows, "chipset").includes("Imaginary chipset"));
assert.ok(!fieldOptions(tabletRows, "pricePhp").length);
assert.ok(fieldOptions(catalogRows("laptops"), "cpu").includes("Intel Core i9-14900HX"));
console.log("Filter options come from recorded values: pass");
passed++;

const sorted = sortRows(catalogRows("laptops"), "price_asc").map(({ device }) => device.id);
assert.deepEqual(sorted, ["acer-aspire-lite-al14-42p", "acer-aspire-lite-al15-33p", "acer-aspire-go-ag15-43p", "acer-swift-go-sfg14-01", "acer-swift-go-sfg14-75", "acer-swift-air-sfa14", "acer-swift-sf14-51", "acer-predator-phn16-72", "acer-predator-phn16s-71", "acer-predator-phn16-73"]);
console.log("Price sort, independently listed order: pass");
passed++;

const fixture: CatalogRow[] = Array.from({ length: 12 }, (_, index) => ({ device: { ...catalogDevices[0], id: `fixture-${index.toString().padStart(2, "0")}` }, variant: { ...catalogDevices[0].variants[0], id: `fixture-variant-${index}` } }));
assert.equal(pageRows(fixture, 0).length, 10);
assert.deepEqual(pageRows(fixture, 1).map(({ device }) => device.id), ["fixture-10", "fixture-11"]);
console.log("First 10 and second page fixture: pass");
passed++;

console.log(`${passed} passed, 0 failed, 0 not assessed`);
