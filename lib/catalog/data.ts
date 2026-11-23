import type { CatalogDevice, CatalogSource, DeviceSpecs } from "./types";

// These dates record when the official Philippine pages were checked. They are not launch dates.
export const CATALOG_OBSERVED_AT = "2026-11-23";
export const CATALOG_VERSION = "2026-11-23-initial-30";

function phSource(organization: string, url: string, note?: string): CatalogSource {
  return { organization, url, observedAt: CATALOG_OBSERVED_AT, purpose: "Specifications and availability", note };
}

function tablet(id: string, brand: string, model: string, variant: string, url: string, specs: DeviceSpecs, notes?: string): CatalogDevice {
  return {
    id, category: "tablets", brand, model, releaseDate: null, philippineAvailabilityDate: null,
    philippineAvailability: "Official Philippine product page observed 23 Nov 2026; original local launch date not verified.",
    discontinued: null, sources: [phSource(brand === "Samsung" ? "Samsung Philippines" : "Xiaomi Philippines", url)],
    variants: [{ id: `${id}-${variant.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`, label: variant, specs,
      pricePhp: null, priceCondition: null, priceObservedAt: null, priceSourceUrl: null,
      listingStatus: "Not verified", notes: notes ?? "Philippine price and lifecycle status have not been verified." }]
  };
}

function phone(id: string, brand: string, model: string, variant: string, url: string, specs: DeviceSpecs, organization = "Xiaomi Philippines"): CatalogDevice {
  return {
    id, category: "smartphones", brand, model, releaseDate: null, philippineAvailabilityDate: null,
    philippineAvailability: "Official Philippine product page observed 23 Nov 2026; original local launch date not verified.",
    discontinued: null, sources: [phSource(organization, url)],
    variants: [{ id: `${id}-${variant.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`, label: variant, specs,
      pricePhp: null, priceCondition: null, priceObservedAt: null, priceSourceUrl: null,
      listingStatus: "Not verified", notes: "Philippine price and lifecycle status have not been verified." }]
  };
}

function laptop(id: string, model: string, sku: string, url: string, pricePhp: number, specs: DeviceSpecs, listingStatus: "In stock" | "Out of stock" = "In stock", notes?: string): CatalogDevice {
  return {
    id, category: "laptops", brand: "Acer", model, releaseDate: null, philippineAvailabilityDate: null,
    philippineAvailability: "Acer Philippines official store listing observed 23 Nov 2026; original local launch date not verified.",
    discontinued: null, sources: [phSource("Acer Philippines Official Store", url)],
    variants: [{ id: `${id}-${sku.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`, label: sku, specs,
      pricePhp, priceCondition: "new", priceObservedAt: CATALOG_OBSERVED_AT, priceSourceUrl: url,
      listingStatus, notes: notes ?? "Observed store price; promotions and stock can change." }]
  };
}

export const catalogDevices: CatalogDevice[] = [
  phone("poco-f7", "POCO", "F7", "12 GB / 256 GB", "https://www.mi.com/ph/product/poco-f7/specs/", { os: "Xiaomi HyperOS 2", chipset: "Snapdragon 8s Gen 4", ramGb: 12, storageGb: 256, storageType: "UFS 4.1", displayInches: 6.83, resolution: "2772 × 1280", refreshHz: 120, rearCameraMp: 50, frontCameraMp: 20, video: "4K 60 fps", batteryMah: 6500, chargingW: 90, weightG: 215.7 }),
  phone("poco-f7-pro", "POCO", "F7 Pro", "12 GB / 256 GB", "https://www.mi.com/ph/product/poco-f7-pro/specs/", { chipset: "Snapdragon 8 Gen 3", ramGb: 12, storageGb: 256, storageType: "UFS 4.1", displayInches: 6.67, displayType: "AMOLED", resolution: "3200 × 1440", refreshHz: 120, rearCameraMp: 50, frontCameraMp: 20, video: "8K 24 fps", batteryMah: 6000, chargingW: 90, weightG: 206 }),
  phone("poco-f7-ultra", "POCO", "F7 Ultra", "12 GB / 256 GB", "https://www.mi.com/ph/product/poco-f7-ultra/specs/", { chipset: "Snapdragon 8 Elite", ramGb: 12, storageGb: 256, displayInches: 6.67, displayType: "AMOLED", resolution: "3200 × 1440", refreshHz: 120, rearCameraMp: 50, frontCameraMp: 32, video: "8K 24 fps", batteryMah: 5300, chargingW: 120, weightG: 212 }),
  phone("poco-x7-pro", "POCO", "X7 Pro", "8 GB / 256 GB", "https://www.mi.com/ph/product/poco-x7-pro/specs/", { chipset: "Dimensity 8400-Ultra", ramGb: 8, storageGb: 256, storageType: "UFS 4.0", displayInches: 6.67, displayType: "AMOLED", resolution: "2712 × 1220", refreshHz: 120, rearCameraMp: 50, frontCameraMp: 20, video: "4K 60 fps", batteryMah: 6000, chargingW: 90 }),
  phone("xiaomi-15", "Xiaomi", "15", "12 GB / 256 GB", "https://www.mi.com/ph/product/xiaomi-15/specs/", { chipset: "Snapdragon 8 Elite", ramGb: 12, storageGb: 256, storageType: "UFS 4.0", displayInches: 6.36, displayType: "AMOLED", resolution: "2670 × 1200", refreshHz: 120, rearCameraMp: 50, video: "8K 30 fps", batteryMah: 5240, chargingW: 90 }),
  phone("xiaomi-15-ultra", "Xiaomi", "15 Ultra", "16 GB / 512 GB", "https://www.mi.com/ph/product/xiaomi-15-ultra/specs/", { chipset: "Snapdragon 8 Elite", ramGb: 16, storageGb: 512, storageType: "UFS 4.1", displayInches: 6.73, displayType: "AMOLED", resolution: "3200 × 1440", refreshHz: 120, rearCameraMp: 50, frontCameraMp: 32, video: "8K 30 fps", batteryMah: 5410, chargingW: 90 }),
  phone("redmi-note-14", "REDMI", "Note 14", "6 GB / 128 GB", "https://www.mi.com/ph/product/redmi-note-14/specs/", { os: "Xiaomi HyperOS", chipset: "Helio G99-Ultra", ramGb: 6, storageGb: 128, storageType: "UFS 2.2", displayInches: 6.67, displayType: "AMOLED", resolution: "2400 × 1080", refreshHz: 120, rearCameraMp: 108, frontCameraMp: 20, video: "1080p 60 fps", batteryMah: 5500, chargingW: 33, weightG: 196.5, cellular: "4G", wifi: "Wi-Fi 5", sim: "Dual SIM" }),
  phone("redmi-note-14-5g", "REDMI", "Note 14 5G", "6 GB / 128 GB", "https://www.mi.com/ph/product/redmi-note-14-5g/specs/", { os: "Xiaomi HyperOS", chipset: "Dimensity 7025-Ultra", ramGb: 6, storageGb: 128, storageType: "UFS 2.2", displayInches: 6.67, displayType: "AMOLED", resolution: "2400 × 1080", refreshHz: 120, rearCameraMp: 108, frontCameraMp: 20, video: "1080p 30 fps", batteryMah: 5110, chargingW: 45, weightG: 190, cellular: "5G", wifi: "Wi-Fi 5", sim: "Dual SIM" }),
  phone("redmi-note-14-pro-5g", "REDMI", "Note 14 Pro 5G", "8 GB / 256 GB", "https://www.mi.com/ph/product/redmi-note-14-pro-5g/specs/", { chipset: "Dimensity 7300-Ultra", ramGb: 8, storageGb: 256, storageType: "UFS 2.2", displayInches: 6.67, displayType: "AMOLED", resolution: "2712 × 1220", refreshHz: 120, rearCameraMp: 200, frontCameraMp: 20, video: "4K 30 fps", batteryMah: 5110, chargingW: 45, weightG: 190, cellular: "5G" }),
  phone("samsung-galaxy-a56-5g", "Samsung", "Galaxy A56 5G", "8 GB / 128 GB · SM-A566BZKSPHL", "https://www.samsung.com/ph/smartphones/galaxy-a/galaxy-a56-5g-awesome-graphite-128gb-sm-a566bzksphl/", { os: "Android", ramGb: 8, storageGb: 128, displayInches: 6.7, displayType: "Super AMOLED", resolution: "1080 × 2340", refreshHz: 120, rearCameraMp: 50, frontCameraMp: 12, video: "4K 30 fps", batteryMah: 5000, weightG: 198, cellular: "5G", wifi: "Wi-Fi 6", sim: "Dual SIM", ports: "USB-C (USB 2.0)" }, "Samsung Philippines"),
  tablet("xiaomi-pad-7", "Xiaomi", "Pad 7", "8 GB / 128 GB", "https://www.mi.com/ph/product/xiaomi-pad-7/specs/", { os: "Xiaomi HyperOS 2", chipset: "Snapdragon 7+ Gen 3", ramGb: 8, storageGb: 128, storageType: "UFS 3.1", displayInches: 11.2, resolution: "3200 × 2136", refreshHz: 144, rearCameraMp: 13, frontCameraMp: 8, video: "4K 30 fps", batteryMah: 8850, chargingW: 45, weightG: 500, wifi: "Wi-Fi 6E", ports: "USB-C (USB 3.2 Gen 1)" }),
  tablet("xiaomi-pad-7-pro", "Xiaomi", "Pad 7 Pro", "8 GB / 256 GB", "https://www.mi.com/ph/product/xiaomi-pad-7-pro/specs/", { os: "Xiaomi HyperOS 2", chipset: "Snapdragon 8s Gen 3", ramGb: 8, storageGb: 256, storageType: "UFS 4.0", displayInches: 11.2, resolution: "3200 × 2136", refreshHz: 144, rearCameraMp: 50, frontCameraMp: 32, video: "4K 60 fps", batteryMah: 8850, chargingW: 67, weightG: 500, wifi: "Wi-Fi 7 capable", ports: "USB-C (USB 3.2 Gen 1)" }),
  tablet("xiaomi-pad-8", "Xiaomi", "Pad 8", "8 GB / 256 GB", "https://www.mi.com/ph/product/xiaomi-pad-8/specs/", { chipset: "Snapdragon 8s Gen 4", ramGb: 8, storageGb: 256, storageType: "UFS 4.1", displayInches: 11.2, resolution: "3200 × 2136", refreshHz: 144, rearCameraMp: 13, frontCameraMp: 8, video: "4K 30 fps", batteryMah: 9200, chargingW: 45, weightG: 485, wifi: "Wi-Fi 7 capable", ports: "USB-C (USB 3.2 Gen 1)" }),
  tablet("xiaomi-pad-8-pro", "Xiaomi", "Pad 8 Pro", "8 GB / 256 GB", "https://www.mi.com/ph/product/xiaomi-pad-8-pro/specs/", { chipset: "Snapdragon 8 Elite", ramGb: 8, storageGb: 256, storageType: "UFS 4.1", displayInches: 11.2, resolution: "3200 × 2136", refreshHz: 144, rearCameraMp: 50, frontCameraMp: 32, video: "4K 60 fps", batteryMah: 9200, chargingW: 67, weightG: 485, wifi: "Wi-Fi 7 capable", ports: "USB-C (USB 3.2 Gen 1)" }),
  tablet("xiaomi-pad-mini", "Xiaomi", "Pad Mini", "8 GB / 256 GB", "https://www.mi.com/ph/product/xiaomi-pad-mini/specs/", { os: "Xiaomi HyperOS 2", chipset: "MediaTek Dimensity 9400+", ramGb: 8, storageGb: 256, storageType: "UFS 4.1", displayInches: 8.8, resolution: "3008 × 1880", refreshHz: 165, rearCameraMp: 13, frontCameraMp: 8, video: "4K 30 fps", batteryMah: 7500, chargingW: 67, weightG: 326, wifi: "Wi-Fi 7 capable", ports: "Two USB-C ports" }),
  tablet("poco-pad-m1", "POCO", "Pad M1", "8 GB / 256 GB", "https://www.mi.com/ph/product/poco-pad-m1/specs/", { os: "Xiaomi HyperOS 2", chipset: "Snapdragon 7s Gen 4", ramGb: 8, storageGb: 256, storageType: "UFS 2.2", displayInches: 12.1, resolution: "2560 × 1600", refreshHz: 120, rearCameraMp: 8, frontCameraMp: 8, video: "1080p 30 fps", batteryMah: 12000, chargingW: 33, weightG: 610, wifi: "Wi-Fi 6", ports: "USB-C (USB 2.0)" }),
  tablet("poco-pad-x1", "POCO", "Pad X1", "8 GB / 512 GB", "https://www.mi.com/ph/product/poco-pad-x1/specs/", { os: "Xiaomi HyperOS 2", chipset: "Snapdragon 7+ Gen 3", ramGb: 8, storageGb: 512, storageType: "UFS 4.0", displayInches: 11.2, resolution: "3200 × 2136", refreshHz: 144, rearCameraMp: 13, frontCameraMp: 8, video: "4K 30 fps", batteryMah: 8850, chargingW: 45, weightG: 500, wifi: "Wi-Fi 6E", ports: "USB-C (USB 3.2 Gen 1)" }),
  tablet("redmi-pad-se-87-4g", "REDMI", "Pad SE 8.7 4G", "4 GB / 64 GB", "https://www.mi.com/ph/product/redmi-pad-se-8-7-inch-4g/specs/", { os: "Xiaomi HyperOS", chipset: "MediaTek Helio G85", ramGb: 4, storageGb: 64, storageType: "eMMC 5.1", displayInches: 8.7, displayType: "LCD", resolution: "1340 × 800", refreshHz: 90, rearCameraMp: 8, frontCameraMp: 5, video: "1080p 30 fps", batteryMah: 6650, chargingW: 18, weightG: 375, wifi: "Wi-Fi 5", cellular: "4G", sim: "Dual SIM", ports: "USB-C (USB 2.0)" }, "Manufacturer lists weight as 375 g or less; 375 g is used as the upper bound."),
  tablet("redmi-pad-2-pro", "REDMI", "Pad 2 Pro", "8 GB / 256 GB", "https://www.mi.com/ph/product/redmi-pad-2-pro/specs/", { os: "Xiaomi HyperOS 2", chipset: "Snapdragon 7s Gen 4", ramGb: 8, storageGb: 256, storageType: "UFS 2.2", displayInches: 12.1, resolution: "2560 × 1600", refreshHz: 120, rearCameraMp: 8, frontCameraMp: 8, video: "1080p 30 fps", batteryMah: 12000, chargingW: 33, weightG: 610, wifi: "Wi-Fi 6", ports: "USB-C (USB 2.0)" }),
  {
    ...tablet("samsung-tab-s10-fe", "Samsung", "Galaxy Tab S10 FE", "Wi-Fi / 8 GB / 128 GB", "https://news.samsung.com/ph/galaxy-tab-s10-fe-series-brings-intelligent-experiences-to-the-forefront-with-premium-versatile-design", { os: "Android 15", chipset: "Exynos 1580", ramGb: 8, storageGb: 128, displayInches: 10.9, displayType: "LCD", refreshHz: 90, rearCameraMp: 13, frontCameraMp: 12, batteryMah: 8000, chargingW: 45, weightG: 497, wifi: "Wi-Fi 6", stylus: "S Pen included", keyboard: "Book Cover Keyboard compatible", dimensions: "254.3 × 165.8 × 6.0 mm" }),
    philippineAvailabilityDate: "2025-05-15", philippineAvailability: "Samsung announced Philippine availability starting 15 May 2025."
  },
  laptop("acer-swift-go-sfg14-75", "Swift Go SFG14-75-55MB", "NX.JNBSP.001", "https://store.acer.com/en-ph/swift-go-sfg14-75-55mb-opi-steam-blue", 61749, { laptopType: "Standard", os: "Windows 11 Home", gpu: "Intel Arc 130V", ramGb: 16, ramType: "LPDDR5X", storageGb: 512, storageType: "NVMe SSD", displayInches: 14, displayType: "OLED", resolution: "1920 × 1200" }, "In stock", "The source gives only 'Intel Core Ultra 5' for CPU; exact model is not verified."),
  laptop("acer-swift-go-sfg14-01", "Swift Go SFG14-01-X2PX", "NX.KYXSP.003", "https://store.acer.com/en-ph/swift-go-sfg14-01-x2px-opi-steel-gray", 54149, { laptopType: "Standard", os: "Windows 11 Home", cpu: "Snapdragon X Plus X1P-42-100", gpu: "Qualcomm Adreno GPU", ramGb: 16, ramType: "LPDDR5X", storageGb: 1024, storageType: "NVMe SSD", displayInches: 14.5, displayType: "IPS", resolution: "1920 × 1200", wifi: "Wi-Fi 7", ports: "USB-C, HDMI dongle" }),
  laptop("acer-swift-sf14-51", "Swift SF14-51-553D", "NX.J2KSP.002", "https://store.acer.com/en-ph/swift-sf14-51-553d-opi-frost-blue", 71249, { laptopType: "Standard", os: "Windows 11 Home", cpu: "Intel Core Ultra 5 228V", gpu: "Intel Arc Graphics", ramGb: 32, storageGb: 1024, storageType: "SSD", displayInches: 14.5, displayType: "OLED" }),
  laptop("acer-aspire-lite-al15-33p", "Aspire Lite AL15-33P-332M", "NX.DY0SP.001", "https://store.acer.com/en-ph/aspire-lite-al15-33p-332m-natural-titanium", 34199, { laptopType: "Standard", os: "Windows 11 Home", cpu: "Intel Core 3 N355", gpu: "Intel UHD Graphics", ramGb: 8, ramType: "LPDDR5", storageGb: 512, storageType: "NVMe SSD", displayInches: 15.6, displayType: "IPS", ports: "USB-C" }),
  laptop("acer-aspire-go-ag15-43p", "Aspire Go 15 AI AG15-43P-R19X", "NX.JPKSP.001", "https://store.acer.com/en-ph/aspire-go-15-ai-ag15-43p-r19x-opi-pure-silver", 53199, { laptopType: "Standard", os: "Windows 11 Home", cpu: "AMD Ryzen 5 7640HS", gpu: "AMD Radeon 680M", ramGb: 16, ramType: "DDR5", storageGb: 512, storageType: "NVMe SSD", displayInches: 15.6, displayType: "IPS", ports: "Two USB-C ports" }),
  laptop("acer-aspire-lite-al14-42p", "Aspire Lite AL14-42P-R1LF", "NX.DJ3SP.001", "https://store.acer.com/en-ph/aspire-lite-al14-42p-r1lf-opi-light-silver", 33249, { laptopType: "Standard", os: "Windows 11 Home", cpu: "AMD Ryzen 3 5300U", gpu: "AMD Radeon Graphics", ramGb: 8, ramType: "DDR4", storageGb: 512, storageType: "NVMe SSD", displayInches: 14, displayType: "IPS", ports: "USB-C" }),
  laptop("acer-predator-phn16-73", "Predator Helios Neo 16 PHN16-73-93Y5", "NH.QX2SP.001", "https://store.acer.com/en-ph/predator-helios-neo-16-phn16-73-93y5-opi-abyssal-black", 204249, { laptopType: "Gaming", os: "Windows 11 Home", cpu: "Intel Core Ultra 9 275HX", gpu: "NVIDIA GeForce RTX 5070 Ti", ramGb: 32, ramMaxGb: 192, storageGb: 1024, storageType: "NVMe SSD", displayInches: 16, keyboard: "RGB backlit" }),
  laptop("acer-swift-air-sfa14", "Swift Air 14 AI SFA14-I31-56FJ", "NX.SHYSP.002", "https://store.acer.com/en-ph/swift-air-14-ai-i-sfa14-i31-56fj-opi-sage-green", 67999, { laptopType: "Standard", os: "Windows 11 Home", cpu: "Intel Core 5 320", gpu: "Intel Graphics", ramGb: 8, ramType: "LPDDR5", storageGb: 512, storageType: "NVMe SSD", displayInches: 14, displayType: "IPS", resolution: "1920 × 1200", batteryWh: 70 }),
  laptop("acer-predator-phn16s-71", "Predator Helios Neo Slim 16 PHN16S-71-9269", "NH.QXASP.003", "https://store.acer.com/en-ph/predator-helios-neo-slim-16-phn16s-71-9269-opi-abyssal-black", 194749, { laptopType: "Gaming", cpu: "Intel Core Ultra 9 275HX", gpu: "NVIDIA GeForce RTX 5070", ramGb: 32, storageGb: 1024, storageType: "SSD", displayInches: 16, displayType: "OLED", keyboard: "RGB backlit" }),
  laptop("acer-predator-phn16-72", "Predator Helios Neo 16 PHN16-72-99K9", "NH.QNNSP.003", "https://store.acer.com/en-ph/intel-corei9-predator-helios-neo-16-phn16-72-99k9-opi-black", 109249, { laptopType: "Gaming", os: "Windows 11 Home", cpu: "Intel Core i9-14900HX", gpu: "NVIDIA GeForce RTX 4060", ramGb: 16, ramType: "DDR5", ramMaxGb: 32, storageGb: 512, storageType: "NVMe SSD", displayInches: 16, displayType: "IPS", resolution: "2560 × 1600", batteryWh: 90, wifi: "Wi-Fi 6E", keyboard: "RGB backlit" }, "Out of stock", "Official listing was out of stock on the product page; listed price is an observed new-product price.")
];

export function devicesForCategory(category: string) {
  return catalogDevices.filter((device) => device.category === category);
}

export function catalogRows(category: string) {
  return devicesForCategory(category).flatMap((device) => device.variants.map((variant) => ({ device, variant })));
}
