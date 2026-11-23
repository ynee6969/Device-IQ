import type { DecisionConstraints } from "@/lib/recommendation/types";

export interface SmartphoneFilterFields {
  brand: string;
  os: string | null;
  price: number;
  battery: number | null;
  ram: number | null;
}

export function exclusionReason(phone: SmartphoneFilterFields, constraints: DecisionConstraints) {
  if (constraints.brands.length && !constraints.brands.includes(phone.brand)) return "Brand";
  if (constraints.minPrice !== undefined && !(phone.price >= constraints.minPrice)) return "Minimum price";
  if (constraints.maxPrice !== undefined && !(phone.price > 0 && phone.price <= constraints.maxPrice)) return "Maximum price";
  if (constraints.minBattery !== undefined && !(phone.battery !== null && phone.battery >= constraints.minBattery)) return "Minimum battery capacity";
  if (constraints.minRam !== undefined && !(phone.ram !== null && phone.ram >= constraints.minRam)) return "Minimum RAM";
  if (constraints.os !== "any" && !phone.os?.toLowerCase().match(/[a-z]+/g)?.includes(constraints.os)) return "Operating system";
  return null;
}

export function filterEligibleSmartphones<TPhone extends SmartphoneFilterFields>(
  phones: readonly TPhone[],
  constraints: DecisionConstraints
) {
  return phones.filter((phone) => exclusionReason(phone, constraints) === null);
}
