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
  observedAt: string;
  publishedAt?: string | null;
  purpose: "Philippine availability" | "Specifications and availability" | "Specifications" | "Price";
  note?: string;
}

export interface DeviceVariant {
  id: string;
  label: string;
  specs: DeviceSpecs;
  specSources?: Partial<Record<SpecKey, string>>;
  pricePhp: number | null;
  priceCondition: "new" | "used" | null;
  priceObservedAt: string | null;
  priceSourceUrl: string | null;
  listingStatus: "In stock" | "Out of stock" | "Not verified";
  notes?: string;
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
