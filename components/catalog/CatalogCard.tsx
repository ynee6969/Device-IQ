import Link from "next/link";
import type { Route } from "next";
import type { CatalogRow, DeviceSpecs } from "@/lib/catalog/types";
import { CatalogProductImage } from "./CatalogProductImage";
import { CatalogSaveButton } from "./CatalogSaveButton";
import { isExcludedRecord, scopeLabel, verificationLabel } from "@/lib/catalog/status";
import { catalogImage } from "@/lib/catalog/images";
import styles from "./catalog.module.css";

function formatPrice(price: number | null) {
  return price === null ? "Not recorded" : new Intl.NumberFormat("en-PH", { style: "currency", currency: "PHP", maximumFractionDigits: 0 }).format(price);
}

function facts(specs: DeviceSpecs, category: CatalogRow["device"]["category"]): [string, string][] {
  const entries: [string, string | number | boolean | undefined][] = category === "laptops"
    ? [["Processor", specs.cpu], ["Graphics", specs.gpu], ["Storage", specs.storageGb ? `${specs.storageGb} GB` : undefined]]
    : [["Chipset", specs.chipset], ["Battery", specs.batteryMah ? `${specs.batteryMah.toLocaleString("en-PH")} mAh` : undefined], ["Camera", specs.rearCameraMp ? `${specs.rearCameraMp} MP main` : undefined]];
  return entries.filter((item): item is [string, string | number | boolean] => item[1] !== undefined).map(([label, value]) => [label, String(value)]);
}

export function CatalogCard({ row, priority = false }: { row: CatalogRow; priority?: boolean }) {
  const { device, variant } = row;
  const excluded = isExcludedRecord(device);
  const detailUrl = `/devices/${device.category}/${device.id}?variant=${encodeURIComponent(variant.id)}`;
  const factsShown = facts(variant.specs, device.category);
  const image = catalogImage(device.imageId ?? device.id);
  return <article className={styles.card}>
    <div className={styles.cardTop}><span className={styles.category}>{device.brand}</span>{!excluded && <CatalogSaveButton variantId={variant.id} />}</div>
    <Link className={styles.cardImageLink} href={detailUrl as Route} aria-label={`View ${device.brand} ${device.model} record`}><CatalogProductImage device={device} priority={priority} /></Link>
    {image?.licenseUrl && <p className={styles.imageCredit}>Image: <a href={image.sourcePage} target="_blank" rel="noreferrer">{image.credit ?? "Source"}</a> · <a href={image.licenseUrl} target="_blank" rel="noreferrer">{image.usageTerms}</a></p>}
    <div className={styles.cardContent}>
      <div className={styles.cardTitle}><div className={styles.statusRow}><span className={`${styles.statusPill} ${excluded ? styles.statusExcluded : device.scopeStatus === "Included" ? styles.statusVerified : styles.statusPending}`}>{scopeLabel(device)}</span><span className={styles.verificationText}>{verificationLabel(device)}</span></div><h2>{device.brand} {device.model}</h2><p className={styles.variant}>{variant.label}</p>{device.qualityFlag && device.qualityFlag !== "Ready for review" && <p className={styles.variant}>Record note: {device.qualityFlag}</p>}{device.recordType === "held_out_claim" && <p className={styles.variant}>Research claim; exact product and local release unconfirmed.</p>}{device.claimedReleaseYear && device.verificationStatus === "PENDING_VERIFICATION" && <p className={styles.variant}>Claimed research year: {device.claimedReleaseYear}</p>}</div>
      <div className={styles.cardHighlights}>
        <div><span>Memory</span><strong>{typeof variant.specs.ramGb === "number" ? `${variant.specs.ramGb} GB RAM` : "Not recorded"}</strong></div>
        <div><span>{variant.priceCondition === "used" ? "Second-hand price" : variant.priceType ?? "Price"}</span><strong>{formatPrice(variant.pricePhp)}</strong></div>
      </div>
      <dl className={styles.quickSpecs}>
        {(variant.specs.displayInches || variant.specs.displayType) && <div><dt>Display</dt><dd>{variant.specs.displayInches ? `${variant.specs.displayInches} in` : ""}{variant.specs.displayType ? ` · ${variant.specs.displayType}` : ""}</dd></div>}
        {factsShown.map(([label, value]) => <div key={label}><dt>{label}</dt><dd>{value}</dd></div>)}
      </dl>
      {!factsShown.length && !variant.specs.displayInches && !variant.specs.displayType && <p className={styles.hint}>Specifications not recorded.</p>}
      <div className={`${styles.cardActions} ${excluded ? styles.singleAction : ""}`}>
        <Link className="button-secondary" href={detailUrl as Route}>View record</Link>
        {!excluded && <Link className="button" href={`/compare?category=${device.category}&first=${encodeURIComponent(variant.id)}`}>Compare</Link>}
      </div>
    </div>
  </article>;
}
