import type { CatalogDevice } from "./types";

export function isExcludedRecord(device: CatalogDevice) {
  return device.scopeStatus === "Excluded" || device.scopeStatus === "Held out";
}

export function verificationLabel(device: CatalogDevice) {
  if (device.verificationStatus === "VERIFIED_OFFICIAL_LAUNCH") return "Official Philippine launch verified";
  if (device.verificationStatus === "VERIFIED_AUTHORIZED_AVAILABILITY") return "Philippine availability verified";
  return "Philippine availability unverified";
}

export function scopeLabel(device: CatalogDevice) {
  if (device.scopeStatus === "Pending date") return "Date unresolved";
  if (device.scopeStatus === "Pending") return "Pending review";
  if (device.scopeStatus === "Included") return "In study scope";
  return device.scopeStatus ?? "Pending review";
}
