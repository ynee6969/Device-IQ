import snapshot from "./public-inventory.json";
import type { CatalogDevice } from "./types";

// Generated from the supplied workbook. The website reads this checked-in snapshot.
export const CATALOG_VERSION = "2026-11-24-workbook-inventory";
export const catalogDevices: CatalogDevice[] = snapshot as CatalogDevice[];

export function devicesForCategory(category: string) {
  return catalogDevices.filter((device) => device.category === category);
}

export function catalogRows(category: string) {
  return devicesForCategory(category).filter((device) => device.scopeStatus !== "Excluded" && device.scopeStatus !== "Held out").flatMap((device) =>
    device.variants.map((variant) => ({ device, variant })));
}

export function excludedDevicesForCategory(category: string) {
  return devicesForCategory(category).filter((device) => device.scopeStatus === "Excluded" || device.scopeStatus === "Held out");
}
