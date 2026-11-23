import imageManifest from "./image-manifest.json";

export interface CatalogImageRecord {
  path: string;
  sourcePage: string;
  assetUrl: string;
  scope: string;
}

const images = imageManifest as Record<string, CatalogImageRecord>;

export function catalogImage(deviceId: string): CatalogImageRecord | null {
  return images[deviceId] ?? null;
}
