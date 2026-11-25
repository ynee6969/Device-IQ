export type DeviceCategory = "smartphones" | "tablets" | "laptops";

export type SpecKey =
  | "os" | "chipset" | "cpu" | "gpu" | "ramGb" | "ramType" | "ramMaxGb"
  | "storageGb" | "storageType" | "displayInches" | "displayType" | "resolution"
  | "refreshHz" | "touchscreen" | "rearCameraMp" | "frontCameraMp" | "video"
  | "batteryMah" | "batteryWh" | "chargingW" | "weightG" | "wifi"
  | "cellular" | "sim" | "ports" | "stylus" | "keyboard" | "dimensions"
  | "laptopType" | "sound";

export type DeviceSpecs = Partial<Record<SpecKey, string | number | boolean>>;

export interface CatalogSource {
  organization: string;
  url: string;
  observedAt: string | null;
  publishedAt?: string | null;
  purpose: string;
  note?: string | null;
}

export interface DeviceVariant {
  id: string;
  label: string;
  specs: DeviceSpecs;
  specSources?: Partial<Record<SpecKey, string>>;
  pricePhp: number | null;
  priceCondition: "new" | "used" | null;
  priceType?: string | null;
  priceObservedAt: string | null;
  priceSourceUrl: string | null;
  listingStatus: "In stock" | "Out of stock" | "Not verified";
  notes?: string | null;
  sku?: string | null;
  modelCode?: string | null;
  workbookRow?: number | null;
}

export interface CatalogDevice {
  id: string;
  category: DeviceCategory;
  brand: string;
  model: string;
  releaseDate: string | null;
  philippineAvailabilityDate: string | null;
  philippineDateLabel?: string;
  philippineReleaseYear?: number | null;
  localEvidenceObservedAt?: string | null;
  verificationStatus?: string;
  scopeStatus?: "Included" | "Pending date" | "Pending" | "Excluded" | "Held out";
  recordType?: "device" | "held_out_claim";
  qualityFlag?: string | null;
  exclusionReason?: string | null;
  exclusionEvidence?: string | null;
  claimedReleaseYear?: number | null;
  manufacturer?: string | null;
  productLine?: string | null;
  modelNumber?: string | null;
  availabilityStatus?: string;
  researchNotes?: string | null;
  openIssues?: { issue: string | null; action: string | null }[];
  workbookRow?: number;
  imageId?: string | null;
  philippineAvailability: string;
  discontinued: boolean | null;
  sources: CatalogSource[];
  variants: DeviceVariant[];
}

export interface CatalogRow {
  device: CatalogDevice;
  variant: DeviceVariant;
}
