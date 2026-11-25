import type { CatalogRow, DeviceCategory, SpecKey } from "./types";
import { scopeLabel, verificationLabel } from "./status";

export type FilterKey = SpecKey | "brand" | "pricePhp" | "priceCondition" | "scopeStatus" | "verificationStatus";
export type FilterDefinition = { key: FilterKey; label: string; group: string; kind: "multi" | "min" | "max"; unit?: string; additional?: boolean; searchable?: boolean };
export type FilterSelections = Record<string, string[] | number | undefined>;
export type CatalogSort = "name_asc" | "name_desc" | "price_asc" | "price_desc" | "ram_desc" | "release_desc";

const common: FilterDefinition[] = [
  { key: "brand", label: "Brand", group: "Basics", kind: "multi" },
  { key: "verificationStatus", label: "Philippine verification", group: "Basics", kind: "multi" },
  { key: "scopeStatus", label: "Research status", group: "Basics", kind: "multi" },
  { key: "pricePhp", label: "Minimum price", group: "Price and condition", kind: "min", unit: "PHP" },
  { key: "pricePhp", label: "Maximum price", group: "Price and condition", kind: "max", unit: "PHP" },
  { key: "priceCondition", label: "Condition", group: "Price and condition", kind: "multi" },
  { key: "os", label: "Operating system", group: "Performance", kind: "multi" },
  { key: "ramGb", label: "Minimum RAM", group: "Performance", kind: "min", unit: "GB" },
  { key: "storageGb", label: "Minimum storage", group: "Performance", kind: "min", unit: "GB" },
  { key: "displayInches", label: "Minimum display size", group: "Display", kind: "min", unit: "in" },
  { key: "displayType", label: "Display technology", group: "Display", kind: "multi" },
  { key: "resolution", label: "Resolution", group: "Display", kind: "multi", additional: true },
  { key: "refreshHz", label: "Minimum refresh rate", group: "Display", kind: "min", unit: "Hz", additional: true },
  { key: "weightG", label: "Maximum weight", group: "Battery and portability", kind: "max", unit: "g", additional: true },
  { key: "wifi", label: "Wi-Fi", group: "Connectivity and compatibility", kind: "multi", additional: true },
  { key: "ports", label: "Ports", group: "Connectivity and compatibility", kind: "multi", additional: true }
];

const mobile: FilterDefinition[] = [
  { key: "chipset", label: "Exact chipset", group: "Performance", kind: "multi", searchable: true },
  { key: "rearCameraMp", label: "Minimum rear camera", group: "Camera and video", kind: "min", unit: "MP", additional: true },
  { key: "frontCameraMp", label: "Minimum front camera", group: "Camera and video", kind: "min", unit: "MP", additional: true },
  { key: "video", label: "Video recording", group: "Camera and video", kind: "multi", additional: true },
  { key: "batteryMah", label: "Minimum battery capacity", group: "Battery and portability", kind: "min", unit: "mAh" },
  { key: "chargingW", label: "Minimum charging power", group: "Battery and portability", kind: "min", unit: "W", additional: true },
  { key: "cellular", label: "Cellular", group: "Connectivity and compatibility", kind: "multi", additional: true },
  { key: "sim", label: "SIM", group: "Connectivity and compatibility", kind: "multi", additional: true }
];

const tablet: FilterDefinition[] = [
  { key: "stylus", label: "Stylus", group: "Connectivity and compatibility", kind: "multi", additional: true },
  { key: "keyboard", label: "Keyboard accessory", group: "Connectivity and compatibility", kind: "multi", additional: true }
];

const laptop: FilterDefinition[] = [
  { key: "laptopType", label: "Laptop type", group: "Basics", kind: "multi" },
  { key: "cpu", label: "Exact CPU", group: "Performance", kind: "multi", searchable: true },
  { key: "gpu", label: "Exact GPU", group: "Performance", kind: "multi", searchable: true },
  { key: "ramType", label: "RAM type", group: "Performance", kind: "multi", additional: true },
  { key: "storageType", label: "Storage type", group: "Performance", kind: "multi", additional: true },
  { key: "batteryWh", label: "Minimum battery capacity", group: "Battery and portability", kind: "min", unit: "Wh", additional: true },
  { key: "keyboard", label: "Keyboard", group: "Connectivity and compatibility", kind: "multi", additional: true }
];

export function filterDefinitions(category: DeviceCategory): FilterDefinition[] {
  return [...common, ...(category === "laptops" ? laptop : mobile), ...(category === "tablets" ? tablet : [])];
}

export function fieldValue(row: CatalogRow, key: FilterKey): string | number | boolean | null {
  if (key === "brand") return row.device.brand;
  if (key === "pricePhp") return row.variant.pricePhp;
  if (key === "priceCondition") return row.variant.priceCondition;
  if (key === "verificationStatus") return verificationLabel(row.device);
  if (key === "scopeStatus") return scopeLabel(row.device);
  return row.variant.specs[key] ?? null;
}

export function fieldOptions(rows: CatalogRow[], key: FilterKey): string[] {
  return [...new Set(rows.map((row) => fieldValue(row, key)).filter((value): value is string | number | boolean => value !== null))]
    .map(String).sort((a, b) => a.localeCompare(b, undefined, { numeric: true }));
}

export function filterRows(rows: CatalogRow[], definitions: FilterDefinition[], selections: FilterSelections): CatalogRow[] {
  return rows.filter((row) => definitions.every((definition) => {
    const selection = selections[`${definition.key}:${definition.kind}`];
    if (selection === undefined || selection === null || (Array.isArray(selection) && selection.length === 0)) return true;
    const value = fieldValue(row, definition.key);
    if (value === null) return false;
    if (definition.kind === "multi") return Array.isArray(selection) && selection.includes(String(value));
    if (typeof selection !== "number" || !Number.isFinite(selection)) return true;
    if (typeof value !== "number") return false;
    return definition.kind === "min" ? value >= selection : value <= selection;
  }));
}

export function sortRows(rows: CatalogRow[], sort: CatalogSort): CatalogRow[] {
  return [...rows].sort((a, b) => {
    const name = `${a.device.brand} ${a.device.model} ${a.variant.label}`.localeCompare(`${b.device.brand} ${b.device.model} ${b.variant.label}`);
    if (sort === "name_asc") return name;
    if (sort === "name_desc") return -name;
    if (sort === "release_desc") return (b.device.releaseDate ?? "").localeCompare(a.device.releaseDate ?? "") || name;
    const left = sort === "ram_desc" ? a.variant.specs.ramGb : a.variant.pricePhp;
    const right = sort === "ram_desc" ? b.variant.specs.ramGb : b.variant.pricePhp;
    if (typeof left !== "number") return typeof right === "number" ? 1 : name;
    if (typeof right !== "number") return -1;
    return (sort === "price_asc" ? left - right : right - left) || name;
  });
}

export function pageRows(rows: CatalogRow[], page: number) {
  const safePage = Math.max(0, Math.floor(page));
  return rows.slice(safePage * 10, safePage * 10 + 10);
}
