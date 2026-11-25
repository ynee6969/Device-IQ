import Image from "next/image";
import { ImageOff } from "lucide-react";
import type { CatalogDevice } from "@/lib/catalog/types";
import { catalogImage } from "@/lib/catalog/images";
import styles from "./catalog.module.css";

export function CatalogProductImage({ device, sizes = "(max-width: 650px) 90vw, 420px", priority = false }: { device: CatalogDevice; sizes?: string; priority?: boolean }) {
  const image = catalogImage(device.imageId ?? device.id);
  return <div className={styles.productImage}>
    {image ? <Image
      src={image.path}
      alt={`${device.brand} ${device.model} product image${image.scope === "Exact model" ? "" : " (pictured color or configuration may vary)"}`}
      fill
      sizes={sizes}
      priority={priority}
      className={styles.productImageElement}
    /> : <span className={styles.imageFallback} role="img" aria-label={`Image unavailable for ${device.brand} ${device.model}`}><ImageOff size={28} aria-hidden="true" /><span>Image unavailable</span></span>}
  </div>;
}
