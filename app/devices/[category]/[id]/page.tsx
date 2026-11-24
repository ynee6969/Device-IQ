import Link from "next/link";
import { notFound } from "next/navigation";
import { devicesForCategory } from "@/lib/catalog/data";
import type { DeviceSpecs, SpecKey } from "@/lib/catalog/types";
import { CatalogSaveButton } from "@/components/catalog/CatalogSaveButton";
import { CatalogProductImage } from "@/components/catalog/CatalogProductImage";
import { catalogImage } from "@/lib/catalog/images";
import styles from "@/components/catalog/catalog.module.css";

const sections: { title: string; fields: [SpecKey, string][] }[] = [
  { title: "Launch and availability", fields: [] },
  { title: "Body", fields: [["dimensions", "Dimensions"], ["weightG", "Weight (g)"], ["laptopType", "Laptop type"]] },
  { title: "Display", fields: [["displayInches", "Size (in)"], ["displayType", "Technology"], ["resolution", "Resolution"], ["refreshHz", "Refresh rate (Hz)"], ["touchscreen", "Touchscreen"]] },
  { title: "Platform", fields: [["os", "Operating system"], ["chipset", "Chipset"], ["cpu", "CPU"], ["gpu", "GPU"]] },
  { title: "Memory", fields: [["ramGb", "RAM (GB)"], ["ramType", "RAM type"], ["ramMaxGb", "Maximum RAM (GB)"], ["storageGb", "Storage (GB)"], ["storageType", "Storage type"]] },
  { title: "Main and front camera", fields: [["rearCameraMp", "Rear camera (MP)"], ["frontCameraMp", "Front camera (MP)"], ["video", "Video"]] },
  { title: "Battery", fields: [["batteryMah", "Capacity (mAh)"], ["batteryWh", "Capacity (Wh)"], ["chargingW", "Charging (W)"]] },
  { title: "Network and communications", fields: [["cellular", "Cellular"], ["sim", "SIM"], ["wifi", "Wi-Fi"], ["ports", "Ports"]] },
  { title: "Features and sound", fields: [["stylus", "Stylus"], ["keyboard", "Keyboard"], ["sound", "Sound"]] }
];

function displayValue(specs: DeviceSpecs, key: SpecKey) {
  const value = specs[key];
  return value === undefined ? "Not recorded" : typeof value === "boolean" ? value ? "Yes" : "No" : String(value);
}

export default async function DevicePage({ params, searchParams }: { params: Promise<{ category: string; id: string }>; searchParams: Promise<{ variant?: string }> }) {
  const { category, id } = await params;
  const { variant: variantId } = await searchParams;
  const device = devicesForCategory(category).find((item) => item.id === id);
  if (!device) notFound();
  const variant = device.variants.find((item) => item.id === variantId) ?? device.variants[0];
  const categoryTitle = category.charAt(0).toUpperCase() + category.slice(1);
  const source = device.sources[0];
  const image = catalogImage(device.imageId ?? device.id);
  const sourceLine = <p className={styles.sourceLine}>Local evidence: <a href={source.url} target="_blank" rel="noreferrer">{source.organization}</a>{source.publishedAt ? ` · published ${source.publishedAt}` : ""} · recorded {source.observedAt}</p>;
  return <section className={`page-shell section ${styles.browser}`}>
    <nav className={styles.breadcrumb} aria-label="Breadcrumb"><Link href="/browse">Categories</Link><span>/</span><Link href={`/browse/${category}`}>{categoryTitle}</Link><span>/</span><span>{device.model}</span></nav>
    <header className={styles.detailHero}>
      <div className={styles.detailImage}><CatalogProductImage device={device} sizes="(max-width: 800px) 90vw, 520px" priority /></div>
      <div className={styles.detailIntro}><span className={styles.eyebrow}>{category.slice(0, -1)}</span><h1>{device.brand} {device.model}</h1><p className={styles.variant}>{variant.label}</p><strong className={styles.detailPrice}>{variant.pricePhp === null ? "Price not recorded" : new Intl.NumberFormat("en-PH", { style: "currency", currency: "PHP", maximumFractionDigits: 0 }).format(variant.pricePhp)}</strong><div className={styles.detailActions}><CatalogSaveButton variantId={variant.id} /><Link className="button" href={`/compare?category=${category}&first=${encodeURIComponent(variant.id)}`}>Compare</Link></div>{image && <p className={styles.sourceLine}>Product image: <a href={image.sourcePage} target="_blank" rel="noreferrer">{image.scope}</a>{image.scope !== "Exact model" ? " · appearance may vary by configuration or color" : ""}</p>}</div>
    </header>
    {device.variants.length > 1 && <nav aria-label="Configurations" className={styles.categories}>{device.variants.map((item) => <Link key={item.id} href={`?variant=${item.id}`}>{item.label}</Link>)}</nav>}
    <div className={styles.detailGrid}>
      <section className={styles.detailSection}><h2>Launch and availability</h2><dl className={styles.specList}><div><dt>Model release date</dt><dd>{device.releaseDate ?? "Not recorded"}</dd></div><div><dt>{device.philippineDateLabel ?? "Philippine availability date"}</dt><dd>{device.philippineAvailabilityDate ?? "Not recorded"}</dd></div><div><dt>Philippine release year</dt><dd>{device.philippineReleaseYear ?? "Not recorded"}</dd></div><div><dt>Local evidence observed by</dt><dd>{device.localEvidenceObservedAt ?? "Not recorded"}</dd></div><div><dt>Verification</dt><dd>{device.verificationStatus === "VERIFIED_OFFICIAL_LAUNCH" ? "Official local launch" : "Official local availability"}</dd></div><div><dt>Local evidence</dt><dd>{device.philippineAvailability}</dd></div><div><dt>Lifecycle</dt><dd>{device.discontinued === true ? "Discontinued" : device.discontinued === false ? "Current" : "Not verified"}</dd></div><div><dt>Store status</dt><dd>{variant.listingStatus}</dd></div></dl>{sourceLine}</section>
      <section className={styles.detailSection}><h2>Price and condition</h2><dl className={styles.specList}><div><dt>{variant.priceCondition === "used" ? "Second-hand price" : "Listed new price"}</dt><dd>{variant.pricePhp === null ? "Not recorded" : new Intl.NumberFormat("en-PH", { style: "currency", currency: "PHP", maximumFractionDigits: 0 }).format(variant.pricePhp)}</dd></div><div><dt>Condition</dt><dd>{variant.priceCondition ?? "Not recorded"}</dd></div><div><dt>Observed</dt><dd>{variant.priceObservedAt ?? "Not recorded"}</dd></div></dl>{variant.notes && <p className={styles.sourceLine}>{variant.notes}</p>}{variant.priceSourceUrl && <p className={styles.sourceLine}>Price source: <a href={variant.priceSourceUrl} target="_blank" rel="noreferrer">View listing</a></p>}</section>
      {sections.slice(1).filter((section) => section.fields.some(([key]) => variant.specs[key] !== undefined)).map((section) => <section className={styles.detailSection} key={section.title}><h2>{section.title}</h2><dl className={styles.specList}>{section.fields.filter(([key]) => variant.specs[key] !== undefined).map(([key, label]) => <div key={key}><dt>{label}</dt><dd>{displayValue(variant.specs, key)}{variant.specSources?.[key] && <> · <a href={variant.specSources[key]} target="_blank" rel="noreferrer">Source</a></>}</dd></div>)}</dl></section>)}
    </div>
  </section>;
}
