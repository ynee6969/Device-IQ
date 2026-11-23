import Link from "next/link";
import type { CatalogRow, DeviceSpecs } from "@/lib/catalog/types";
import { CatalogProductImage } from "./CatalogProductImage";
import { CatalogSaveButton } from "./CatalogSaveButton";
import styles from "./catalog.module.css";

function formatPrice(price: number | null) {
  return price === null ? "Not verified" : new Intl.NumberFormat("en-PH", { style: "currency", currency: "PHP", maximumFractionDigits: 0 }).format(price);
}

function facts(specs: DeviceSpecs, category: CatalogRow["device"]["category"]): [string, string][] {
  const entries: [string, string | number | boolean | undefined][] = category === "laptops"
    ? [["Processor", specs.cpu], ["Graphics", specs.gpu], ["Storage", specs.storageGb ? `${specs.storageGb} GB` : undefined]]
    : [["Chipset", specs.chipset], ["Battery", specs.batteryMah ? `${specs.batteryMah.toLocaleString("en-PH")} mAh` : undefined], ["Camera", specs.rearCameraMp ? `${specs.rearCameraMp} MP main` : undefined]];
  return entries.filter((item): item is [string, string | number | boolean] => item[1] !== undefined).map(([label, value]) => [label, String(value)]);
}

export function CatalogCard({ row, priority = false }: { row: CatalogRow; priority?: boolean }) {
  const { device, variant } = row;
  return <article className={styles.card}>
    <div className={styles.cardTop}><span className={styles.category}>{device.brand}</span><CatalogSaveButton variantId={variant.id} /></div>
    <Link className={styles.cardImageLink} href={`/devices/${device.category}/${device.id}`} aria-label={`View ${device.brand} ${device.model} specifications`}><CatalogProductImage device={device} priority={priority} /></Link>
    <div className={styles.cardContent}>
      <div className={styles.cardTitle}><h2>{device.brand} {device.model}</h2><p className={styles.variant}>{variant.label}</p></div>
      <div className={styles.cardHighlights}>
        <div><span>Memory</span><strong>{variant.specs.ramGb ? `${variant.specs.ramGb} GB RAM` : "Not verified"}</strong></div>
        <div><span>{variant.priceCondition === "used" ? "Used price" : "Listed price"}</span><strong>{formatPrice(variant.pricePhp)}</strong></div>
      </div>
      <dl className={styles.quickSpecs}>
        <div><dt>Display</dt><dd>{variant.specs.displayInches ? `${variant.specs.displayInches} in` : "Not verified"}{variant.specs.displayType ? ` · ${variant.specs.displayType}` : ""}</dd></div>
        {facts(variant.specs, device.category).map(([label, value]) => <div key={label}><dt>{label}</dt><dd>{value}</dd></div>)}
      </dl>
      <div className={styles.cardActions}>
        <Link className="button-secondary" href={`/devices/${device.category}/${device.id}`}>Full specs</Link>
        <Link className="button" href={`/compare?category=${device.category}&first=${encodeURIComponent(variant.id)}`}>Compare</Link>
      </div>
    </div>
  </article>;
}
