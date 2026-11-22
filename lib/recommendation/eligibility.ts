import type { DecisionConstraints } from "@/lib/recommendation/types";

export interface SmartphoneFilterFields {
  brand: string;
  os: string | null;
  price: number;
  battery: number | null;
  ram: number | null;
}

function inferOs(phone: Pick<SmartphoneFilterFields, "brand" | "os">) {
  if (phone.brand.toLowerCase() === "apple" || phone.os?.toLowerCase().includes("ios")) {
    return "ios";
  }
  return "android";
}

export function isSmartphoneEligible<TPhone extends SmartphoneFilterFields>(
  phone: TPhone,
  constraints: DecisionConstraints
) {
  if (constraints.brands.length > 0 && !constraints.brands.includes(phone.brand)) {
    return false;
  }
  if (constraints.minPrice !== undefined && phone.price < constraints.minPrice) {
    return false;
  }
  if (constraints.maxPrice !== undefined && phone.price > constraints.maxPrice) {
    return false;
  }
  if (constraints.minBattery !== undefined && (phone.battery === null || phone.battery < constraints.minBattery)) {
    return false;
  }
  if (constraints.minRam !== undefined && (phone.ram === null || phone.ram < constraints.minRam)) {
    return false;
  }
  return constraints.os === "any" || inferOs(phone) === constraints.os;
}

export function filterEligibleSmartphones<TPhone extends SmartphoneFilterFields>(
  phones: readonly TPhone[],
  constraints: DecisionConstraints
) {
  return phones.filter((phone) => isSmartphoneEligible(phone, constraints));
}
