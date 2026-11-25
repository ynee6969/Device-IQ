import Link from "next/link";
import { notFound } from "next/navigation";
import { devicesForCategory } from "@/lib/catalog/data";
import type { CatalogDevice, DeviceSpecs, SpecKey } from "@/lib/catalog/types";
import { isExcludedRecord, scopeLabel, verificationLabel } from "@/lib/catalog/status";
import { CatalogSaveButton } from "@/components/catalog/CatalogSaveButton";
import { CatalogProductImage } from "@/components/catalog/CatalogProductImage";
import { catalogImage } from "@/lib/catalog/images";
import styles from "@/components/catalog/catalog.module.css";

const sections: { title: string; categories?: string[]; fields: [SpecKey, string][] }[] = [
  { title: "Body and design", fields: [["dimensions", "Dimensions"], ["weightG", "Weight (g)"]] },
  { title: "Display", fields: [["displayInches", "Size (in)"], ["displayType", "Technology"], ["resolution", "Resolution"], ["refreshHz", "Refresh rate (Hz)"]] },
  { title: "Platform", fields: [["os", "Operating system"], ["chipset", "Chipset"], ["cpu", "CPU"], ["gpu", "Graphics"]] },
  { title: "Memory and storage", fields: [["ramGb", "RAM (GB)"], ["storageGb", "Storage (GB)"], ["ramType", "RAM type"], ["storageType", "Storage type"]] },
  { title: "Camera", categories: ["smartphones", "tablets"], fields: [["rearCameraMp", "Rear camera (MP)"], ["frontCameraMp", "Front camera (MP)"], ["video", "Video"]] },
  { title: "Battery", fields: [["batteryMah", "Capacity (mAh)"], ["batteryWh", "Capacity (Wh)"], ["chargingW", "Charging (W)"]] },
  { title: "Connectivity", fields: [["cellular", "Cellular"], ["wifi", "Wi-Fi"], ["ports", "Ports"]] },
];

function displayValue(specs: DeviceSpecs, key: SpecKey) {
  const value = specs[key];
  return value === undefined || value === null ? "Not recorded" : typeof value === "boolean" ? value ? "Yes" : "No" : String(value);
}

function priceLabel(price: number | null) {
  return price === null ? "Not recorded" : new Intl.NumberFormat("en-PH", { style: "currency", currency: "PHP", maximumFractionDigits: 0 }).format(price);
}

function statusClass(device: CatalogDevice) {
  return isExcludedRecord(device) ? styles.statusExcluded : device.scopeStatus === "Included" ? styles.statusVerified : styles.statusPending;
}

export default async function DevicePage({ params, searchParams }: { params: Promise<{ category: string; id: string }>; searchParams: Promise<{ variant?: string }> }) {
  const { category, id } = await params;
  const { variant: variantId } = await searchParams;
  const device = devicesForCategory(category).find((item) => item.id === id);
  if (!device) notFound();
  const variant = device.variants.find((item) => item.id === variantId) ?? device.variants[0];
  const excluded = isExcludedRecord(device);
  const categoryTitle = category.charAt(0).toUpperCase() + category.slice(1);
  const image = catalogImage(device.imageId ?? device.id);
  const visibleSections = sections.filter((section) => !section.categories || section.categories.includes(category)).map((section) => ({
    ...section,
    fields: section.fields.filter(([key]) => !(category === "laptops" && ["chipset", "batteryMah", "chargingW", "cellular"].includes(key)) && !(category !== "laptops" && ["cpu", "gpu", "batteryWh", "ramType", "storageType"].includes(key))),
  })).filter((section) => section.fields.some(([key]) => variant.specs[key] !== undefined));

  return <section className={`page-shell section ${styles.browser}`}>
    <nav className={styles.breadcrumb} aria-label="Breadcrumb"><Link href="/browse">Categories</Link><span>/</span><Link href={`/browse/${category}`}>{categoryTitle}</Link><span>/</span><span>{device.model}</span></nav>
    <header className={styles.detailHero}>
      <div className={styles.detailImage}><CatalogProductImage device={device} sizes="(max-width: 800px) 90vw, 520px" priority /></div>
      <div className={styles.detailIntro}>
        <span className={styles.eyebrow}>{device.recordType === "held_out_claim" ? "Research claim" : category.slice(0, -1)}</span>
        <h1>{device.brand} {device.model}</h1>
        <div className={styles.statusRow}><span className={`${styles.statusPill} ${statusClass(device)}`}>{scopeLabel(device)}</span><span className={styles.verificationText}>{verificationLabel(device)}</span></div>
        {device.qualityFlag && <p className={styles.variant}>Record quality: {device.qualityFlag}</p>}
        <p className={styles.variant}>{variant.label}</p>
        <strong className={styles.detailPrice}>{variant.pricePhp === null ? "Price not recorded" : priceLabel(variant.pricePhp)}</strong>
        {excluded && <p className={styles.exclusionNotice}>{device.exclusionReason ?? "This record is outside the selected research scope."}</p>}
        {!excluded && <div className={styles.detailActions}><CatalogSaveButton variantId={variant.id} /><Link className="button" href={`/compare?category=${category}&first=${encodeURIComponent(variant.id)}`}>Compare</Link></div>}
        <p className={styles.sourceLine}>{image ? <>Product image: <a href={image.sourcePage} target="_blank" rel="noreferrer">{image.scope}{image.credit ? ` · ${image.credit}` : ""}</a>{image.usageTerms && <> · {image.licenseUrl ? <a href={image.licenseUrl} target="_blank" rel="noreferrer">{image.usageTerms}</a> : image.usageTerms}</>}{image.changes ? ` · ${image.changes}` : ""}</> : "Product image unavailable"}</p>
      </div>
    </header>
    {device.variants.length > 1 && <nav aria-label="Configurations" className={styles.variantNav}>{device.variants.map((item) => <Link className={item.id === variant.id ? styles.activeVariant : ""} key={item.id} href={`?variant=${encodeURIComponent(item.id)}`}>{item.label}</Link>)}</nav>}
    <div className={styles.detailGrid}>
      <section className={styles.detailSection}><h2>Research and availability</h2><dl className={styles.specList}>
        <div><dt>Verification</dt><dd>{verificationLabel(device)}</dd></div>
        <div><dt>Research status</dt><dd>{scopeLabel(device)}</dd></div>
        <div><dt>Global release date</dt><dd>{device.releaseDate ?? "Not recorded"}</dd></div>
        <div><dt>{device.philippineDateLabel ?? "Philippine availability date"}</dt><dd>{device.philippineAvailabilityDate ?? "Not recorded"}</dd></div>
        <div><dt>Verified Philippine year</dt><dd>{device.philippineReleaseYear ?? "Not recorded"}</dd></div>
        {device.claimedReleaseYear && <div><dt>Claimed research year</dt><dd>{device.claimedReleaseYear} (unverified as a Philippine release date)</dd></div>}
        <div><dt>Local evidence observed</dt><dd>{device.localEvidenceObservedAt ?? "Not recorded"}</dd></div>
        <div><dt>Availability status</dt><dd>{device.availabilityStatus ?? "Not recorded"}</dd></div>
        <div><dt>Local evidence</dt><dd>{device.philippineAvailability}</dd></div>
        <div><dt>Store status</dt><dd>{variant.listingStatus}</dd></div>
      </dl></section>
      <section className={styles.detailSection}><h2>Price and configuration</h2><dl className={styles.specList}>
        <div><dt>Configuration</dt><dd>{variant.label}</dd></div>
        <div><dt>SKU</dt><dd>{variant.sku ?? "Not recorded"}</dd></div>
        <div><dt>Model code</dt><dd>{variant.modelCode ?? device.modelNumber ?? "Not recorded"}</dd></div>
        <div><dt>Price</dt><dd>{priceLabel(variant.pricePhp)}</dd></div>
        <div><dt>Price type</dt><dd>{variant.priceType ?? "Not recorded"}</dd></div>
        <div><dt>Condition</dt><dd>{variant.priceCondition ?? "Not recorded"}</dd></div>
        <div><dt>Price observed</dt><dd>{variant.priceObservedAt ?? "Not recorded"}</dd></div>
      </dl>{variant.priceSourceUrl && <p className={styles.sourceLine}>Price source: <a href={variant.priceSourceUrl} target="_blank" rel="noreferrer">View source</a></p>}{variant.notes && <p className={styles.sourceLine}>{variant.notes}</p>}</section>
      {visibleSections.length ? visibleSections.map((section) => <section className={styles.detailSection} key={section.title}><h2>{section.title}</h2><dl className={styles.specList}>{section.fields.map(([key, label]) => <div key={key}><dt>{label}</dt><dd>{displayValue(variant.specs, key)}{variant.specSources?.[key] && <> · <a href={variant.specSources[key]} target="_blank" rel="noreferrer">Source</a></>}</dd></div>)}</dl></section>) : <section className={styles.detailSection}><h2>Specifications</h2><p className={styles.sourceLine}>Not recorded in the inventory.</p></section>}
      <section className={styles.detailSection}><h2>Sources and record notes</h2>
        {device.sources.length ? <ul className={styles.sourceList}>{device.sources.map((source) => <li key={source.url}><a href={source.url} target="_blank" rel="noreferrer">{source.organization}</a><span>{source.purpose}{source.observedAt ? ` · checked ${source.observedAt}` : ""}</span>{source.note && <small>{source.note}</small>}</li>)}</ul> : <p className={styles.sourceLine}>Source URL not recorded in the workbook.</p>}
        {device.researchNotes && <p className={styles.sourceLine}>{device.researchNotes}</p>}
        {device.exclusionEvidence && <p className={styles.sourceLine}>Exclusion evidence: {device.exclusionEvidence}</p>}
        {device.openIssues?.length ? <div className={styles.openIssues}><h3>Unresolved research items</h3><ul>{device.openIssues.map((item, index) => <li key={index}>{item.issue ?? "Review pending"}{item.action ? ` · ${item.action}` : ""}</li>)}</ul></div> : null}
        <p className={styles.sourceLine}>Workbook row: {device.workbookRow ?? "Not recorded"}</p>
      </section>
    </div>
  </section>;
}
