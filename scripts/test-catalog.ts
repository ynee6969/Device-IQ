import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { CATALOG_VERSION, catalogDevices, catalogRows } from "../lib/catalog/pilot";
import { catalogDevices as publicDevices, catalogRows as publicRows, excludedDevicesForCategory } from "../lib/catalog/data";
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

assert.equal(publicDevices.length, 463);
assert.deepEqual(["smartphones", "tablets", "laptops"].map((category) =>
  publicDevices.filter((device) => device.category === category).length), [292, 153, 18]);
assert.deepEqual(["smartphones", "tablets", "laptops"].map((category) => publicRows(category).length), [376, 167, 22]);
assert.equal(publicDevices.reduce((count, device) => count + device.variants.length, 0), 575);
const redmagic7Pro = publicDevices.find((device) => device.id === "device_5e189eced7d16d");
assert.ok(redmagic7Pro);
assert.equal(redmagic7Pro.modelNumber, "NX709J");
assert.equal(redmagic7Pro.scopeStatus, "Pending");
assert.equal(redmagic7Pro.verificationStatus, "VERIFIED_AUTHORIZED_AVAILABILITY");
assert.deepEqual(redmagic7Pro.variants.map((variant) => variant.label), [
  "16 GB RAM / 256 GB storage (Obsidian)",
  "16 GB RAM / 512 GB storage (Supernova)",
]);
assert.ok(redmagic7Pro.variants.every((variant) => variant.pricePhp === null));
const nord2 = publicDevices.find((device) => device.id === "device_15827b1eab335d");
assert.ok(nord2);
assert.equal(nord2.scopeStatus, "Pending");
assert.equal(nord2.verificationStatus, "VERIFIED_AUTHORIZED_AVAILABILITY");
assert.deepEqual(nord2.variants.map((variant) => variant.label), [
  "8 GB RAM / 128 GB storage — Blue Haze", "12 GB RAM / 256 GB storage — Gray Sierra",
]);
assert.ok(nord2.variants.every((variant) => variant.pricePhp === null));
const oppoReno5 = publicDevices.find((device) => device.id === "device_914fe6b0343102");
assert.ok(oppoReno5);
assert.equal(oppoReno5.model, "Reno5 4G");
assert.equal(oppoReno5.modelNumber, "CPH2159");
assert.equal(oppoReno5.philippineAvailabilityDate, "2021-02-20");
assert.equal(oppoReno5.scopeStatus, "Pending");
assert.equal(oppoReno5.verificationStatus, "VERIFIED_AUTHORIZED_AVAILABILITY");
assert.deepEqual(oppoReno5.variants.map((variant) => variant.label), ["8 GB RAM / 128 GB storage"]);
assert.equal(oppoReno5.variants[0]?.pricePhp, null);
const oppoReno6 = publicDevices.find((device) => device.id === "device_97f548edfe54b5");
assert.ok(oppoReno6);
assert.equal(oppoReno6.model, "Reno6 5G");
assert.equal(oppoReno6.modelNumber, "CPH2251");
assert.equal(oppoReno6.philippineAvailabilityDate, "2021-08-28");
assert.equal(oppoReno6.scopeStatus, "Pending");
assert.equal(oppoReno6.verificationStatus, "VERIFIED_AUTHORIZED_AVAILABILITY");
assert.deepEqual(oppoReno6.variants.map((variant) => variant.label), ["8 GB RAM / 128 GB storage"]);
assert.equal(oppoReno6.variants[0]?.modelCode, "CPH2251");
assert.equal(oppoReno6.variants[0]?.pricePhp, null);
assert.equal(oppoReno6.variants[0]?.specs.chipset, "MediaTek Dimensity 900");
assert.equal(oppoReno6.variants[0]?.specs.batteryMah, 4300);
assert.equal(oppoReno6.imageId, null);
assert.ok(oppoReno6.sources.some((source) => source.url.includes("ntc.gov.ph") && source.note?.includes("CPH2251")));
const cherryAquaSv = publicDevices.find((device) => device.id === "device_35bc65487e1514");
assert.ok(cherryAquaSv);
assert.equal(cherryAquaSv.model, "Aqua SV 5G");
assert.equal(cherryAquaSv.modelNumber, null);
assert.equal(cherryAquaSv.releaseDate, null);
assert.equal(cherryAquaSv.philippineAvailabilityDate, "2022-04-29");
assert.equal(cherryAquaSv.scopeStatus, "Pending");
assert.equal(cherryAquaSv.verificationStatus, "VERIFIED_AUTHORIZED_AVAILABILITY");
assert.deepEqual(cherryAquaSv.variants.map((variant) => variant.label), ["8 GB RAM / 128 GB storage"]);
assert.equal(cherryAquaSv.variants[0]?.pricePhp, null);
assert.equal(cherryAquaSv.variants[0]?.specs.chipset, "MediaTek Dimensity 810");
assert.equal(cherryAquaSv.variants[0]?.specs.batteryMah, 4200);
assert.equal(cherryAquaSv.variants[0]?.specs.storageType, "UFS 2.2");
assert.equal(cherryAquaSv.imageId, null);
assert.ok(cherryAquaSv.sources.some((source) => source.url.includes("ntc.gov.ph") && source.note?.includes("AQUA SV")));
const coolpadCool20Plus = publicDevices.find((device) => device.id === "device_14031d3cddb48d");
assert.ok(coolpadCool20Plus);
assert.equal(coolpadCool20Plus.model, "COOL 20+");
assert.equal(coolpadCool20Plus.modelNumber, null);
assert.equal(coolpadCool20Plus.releaseDate, null);
assert.equal(coolpadCool20Plus.philippineAvailabilityDate, "2023-10-05");
assert.equal(coolpadCool20Plus.scopeStatus, "Pending");
assert.equal(coolpadCool20Plus.verificationStatus, "VERIFIED_AUTHORIZED_AVAILABILITY");
assert.deepEqual(coolpadCool20Plus.variants.map((variant) => variant.label), ["6 GB RAM / 128 GB storage"]);
assert.equal(coolpadCool20Plus.variants[0]?.pricePhp, null);
assert.equal(coolpadCool20Plus.variants[0]?.specs.chipset, "MediaTek Helio G85");
assert.equal(coolpadCool20Plus.variants[0]?.specs.gpu, "Arm Mali-G52 MC2");
assert.equal(coolpadCool20Plus.variants[0]?.specs.batteryMah, 4500);
assert.equal(coolpadCool20Plus.imageId, null);
assert.ok(coolpadCool20Plus.sources.some((source) => source.url.includes("yugatech.com") && source.note?.includes("6 GB / 128 GB")));
const coolpadCp12 = publicDevices.find((device) => device.id === "device_5bc54f4d744bec");
assert.ok(coolpadCp12);
assert.equal(coolpadCp12.model, "CP12");
assert.equal(coolpadCp12.modelNumber, null);
assert.equal(coolpadCp12.releaseDate, null);
assert.equal(coolpadCp12.philippineAvailabilityDate, "2023-10-05");
assert.equal(coolpadCp12.scopeStatus, "Pending");
assert.equal(coolpadCp12.verificationStatus, "VERIFIED_AUTHORIZED_AVAILABILITY");
assert.equal(coolpadCp12.workbookRow, 134);
assert.deepEqual(coolpadCp12.variants.map((variant) => variant.label), [
  "4 GB RAM / 64 GB storage", "4 GB RAM / 128 GB storage",
]);
assert.ok(coolpadCp12.variants.every((variant) => variant.pricePhp === null));
assert.deepEqual(coolpadCp12.variants.map((variant) => [variant.specs.ramGb, variant.specs.storageGb]), [[4, 64], [4, 128]]);
assert.equal(coolpadCp12.variants[0]?.specs.storageType, undefined);
assert.equal(coolpadCp12.variants[1]?.specs.storageType, "eMMC 5.1");
assert.ok(coolpadCp12.variants.every((variant) => variant.specs.batteryMah === 4500 && variant.specs.chipset === "UNISOC SC9863A"));
assert.ok(coolpadCp12.variants.every((variant) => {
  const specs = variant.specs as Record<string, unknown>;
  return specs.bluetooth === null && specs.sound === null;
}));
assert.equal(coolpadCp12.imageId, null);
assert.ok(coolpadCp12.sources.some((source) => source.url.includes("yugatech.com") && source.note?.includes("64 GB / 128 GB")));
const cp12Prices = JSON.parse(readFileSync(new URL("../research/enrichment/coolpad-cp12-ph-price-candidate-2026-11-26.json", import.meta.url), "utf8"));
assert.deepEqual(cp12Prices.prices.map((price: { variant_storage_gb: number; amount_php: number }) => [price.variant_storage_gb, price.amount_php]), [[64, 3899], [128, 4299]]);
const tecnoCamon17p = publicDevices.find((device) => device.id === "device_097c07418374a0");
assert.ok(tecnoCamon17p);
assert.equal(tecnoCamon17p.model, "Camon 17P");
assert.equal(tecnoCamon17p.modelNumber, "CG7");
assert.equal(tecnoCamon17p.releaseDate, "2021-05-28");
assert.equal(tecnoCamon17p.philippineAvailabilityDate, "2021-06-30");
assert.equal(tecnoCamon17p.scopeStatus, "Pending");
assert.equal(tecnoCamon17p.verificationStatus, "VERIFIED_AUTHORIZED_AVAILABILITY");
assert.equal(tecnoCamon17p.workbookRow, 38);
assert.deepEqual(tecnoCamon17p.variants.map((variant) => variant.label), ["6 GB RAM / 128 GB storage"]);
assert.equal(tecnoCamon17p.variants[0]?.pricePhp, null);
assert.equal(tecnoCamon17p.variants[0]?.modelCode, "CG7");
assert.equal(tecnoCamon17p.variants[0]?.specs.ramGb, 6);
assert.equal(tecnoCamon17p.variants[0]?.specs.storageGb, 128);
assert.equal(tecnoCamon17p.variants[0]?.specs.chipset, "MediaTek Helio G85");
assert.equal(tecnoCamon17p.variants[0]?.specs.batteryMah, 5000);
assert.equal(tecnoCamon17p.variants[0]?.specs.video, null);
assert.equal(tecnoCamon17p.imageId, null);
assert.ok(tecnoCamon17p.sources.some((source) => source.url.includes("ntc.gov.ph") && source.note?.includes("TECNO CG7")));
const camon17pPrices = JSON.parse(readFileSync(new URL("../research/enrichment/tecno-camon-17p-ph-price-candidate-2026-11-26.json", import.meta.url), "utf8"));
assert.deepEqual(camon17pPrices.prices.map((price: { variant_storage_gb: number; amount_php: number }) => [price.variant_storage_gb, price.amount_php]), [[128, 8490]]);
const blackShark4 = publicDevices.find((device) => device.id === "device_fa4c0f6cdc39f6");
assert.ok(blackShark4);
assert.deepEqual(blackShark4.variants.map((variant) => variant.label), [
  "6 GB RAM / 128 GB storage", "8 GB RAM / 128 GB storage",
  "12 GB RAM / 128 GB storage", "12 GB RAM / 256 GB storage",
]);
const blackShark4Eight128 = blackShark4.variants.find((variant) => variant.specs.ramGb === 8 && variant.specs.storageGb === 128);
assert.equal(blackShark4Eight128?.pricePhp, 20545);
assert.equal(blackShark4Eight128?.priceCondition, null);
assert.equal(blackShark4Eight128?.priceType, "KIMSTORE listing observed 2026-11-26; one unit left; condition not stated");
assert.equal(blackShark4Eight128?.listingStatus, "In stock");
const blackShark5 = publicDevices.find((device) => device.id === "device_a9d69522a3d0fe");
assert.ok(blackShark5);
assert.equal(blackShark5.modelNumber, "SHARK PAR-H0");
assert.equal(blackShark5.releaseDate, "2022-06-09");
assert.equal(blackShark5.philippineAvailabilityDate, "2022-07-02");
assert.equal(blackShark5.verificationStatus, "VERIFIED_AUTHORIZED_AVAILABILITY");
assert.equal(blackShark5.scopeStatus, "Pending");
assert.deepEqual(blackShark5.variants.map((variant) => variant.label), [
  "8 GB RAM / 128 GB storage", "12 GB RAM / 256 GB storage",
]);
const blackShark5Eight128 = blackShark5.variants.find((variant) => variant.specs.ramGb === 8 && variant.specs.storageGb === 128);
const blackShark5Twelve256 = blackShark5.variants.find((variant) => variant.specs.ramGb === 12 && variant.specs.storageGb === 256);
assert.equal(blackShark5Eight128?.pricePhp, 24995);
assert.equal(blackShark5Eight128?.priceCondition, null);
assert.equal(blackShark5Eight128?.listingStatus, "In stock");
assert.equal(blackShark5Twelve256?.pricePhp, 32450);
assert.equal(blackShark5Twelve256?.priceCondition, null);
assert.equal(blackShark5Twelve256?.listingStatus, "In stock");
assert.equal(blackShark5Eight128?.specs.rearCameraMp, null);
assert.equal(blackShark5Eight128?.specs.frontCameraMp, null);
assert.equal(blackShark5Eight128?.specs.sound, null);
const blackShark5Pro = publicDevices.find((device) => device.id === "device_abadb9044528e9");
assert.ok(blackShark5Pro);
assert.equal(blackShark5Pro.modelNumber, "SHARK KTUS-H0");
assert.equal(blackShark5Pro.releaseDate, "2022-06-09");
assert.equal(blackShark5Pro.philippineAvailabilityDate, "2022-07-02");
assert.equal(blackShark5Pro.verificationStatus, "VERIFIED_AUTHORIZED_AVAILABILITY");
assert.equal(blackShark5Pro.scopeStatus, "Pending");
assert.deepEqual(blackShark5Pro.variants.map((variant) => variant.label), [
  "8 GB RAM / 128 GB storage", "12 GB RAM / 256 GB storage",
]);
assert.ok(blackShark5Pro.variants.every((variant) => variant.pricePhp === null));
assert.ok(blackShark5Pro.variants.every((variant) => variant.specs.rearCameraMp === null && variant.specs.frontCameraMp === null && variant.specs.wifi === null));
assert.equal(blackShark5Pro.imageId, null);
const motoG50 = publicDevices.find((device) => device.id === "device_195cb093808ae0");
assert.ok(motoG50);
assert.equal(motoG50.model, "Moto G50");
assert.equal(motoG50.productLine, "Moto G50 5G");
assert.equal(motoG50.modelNumber, "XT2149-1");
assert.equal(motoG50.releaseDate, "2021-08-20");
assert.equal(motoG50.philippineAvailabilityDate, "2021-08-30");
assert.equal(motoG50.scopeStatus, "Pending");
assert.deepEqual(motoG50.variants.map((variant) => variant.label), ["4 GB RAM / 128 GB storage"]);
assert.equal(motoG50.variants[0]?.specs.chipset, "MediaTek Dimensity 700");
assert.equal(motoG50.variants[0]?.pricePhp, 10899);
assert.equal(motoG50.variants[0]?.priceCondition, null);
assert.equal(motoG50.variants[0]?.listingStatus, "In stock");
assert.equal(motoG50.imageId, null);
assert.deepEqual(Object.fromEntries(["Included", "Pending date", "Pending", "Excluded", "Held out"].map((status) => [status, publicDevices.filter((device) => device.scopeStatus === status).length])), { Included: 28, "Pending date": 29, Pending: 396, Excluded: 3, "Held out": 7 });
assert.ok(publicDevices.every((device) => device.variants.length &&
  device.sources.every((source) => source.url.startsWith("https://"))));
assert.ok(publicDevices.every((device) => device.variants.every((variant) =>
  variant.pricePhp === null || Boolean(variant.priceType && variant.priceSourceUrl && variant.priceObservedAt))));
assert.ok(publicDevices.some((device) => device.model === "Galaxy S21 5G"));
assert.ok(excludedDevicesForCategory("smartphones").some((device) => device.model === "Galaxy S21 5G"));
assert.ok(excludedDevicesForCategory("tablets").some((device) => device.model === "ASUS Pad" && device.recordType === "held_out_claim"));
assert.ok(!publicRows("smartphones").some((row) => row.device.model === "Galaxy S21 5G"));
for (const category of ["smartphones", "tablets", "laptops"] as const) {
  const excludedIds = new Set(excludedDevicesForCategory(category).map((device) => device.id));
  assert.ok(publicRows(category).every((row) => !excludedIds.has(row.device.id)));
}
assert.equal(filterRows(publicRows("smartphones"), filterDefinitions("smartphones"), { "pricePhp:max": 20000 }).some((row) => row.variant.pricePhp === null), false);
assert.equal(pageRows(sortRows(publicRows("smartphones"), "name_asc"), 0).length, 10);
assert.equal(pageRows(sortRows(publicRows("smartphones"), "name_asc"), 1).length, 10);
console.log("Workbook inventory coverage, exclusion boundaries, variants, provenance and pagination: pass");
passed++;

console.log(`${passed} passed, 0 failed, 0 not assessed`);
