import Link from "next/link";
import { devicesForCategory } from "@/lib/catalog/data";
import { CatalogProductImage } from "@/components/catalog/CatalogProductImage";
import styles from "@/components/catalog/catalog.module.css";

const categories = [
  { slug: "smartphones", title: "Smartphones", copy: "Chipset, camera, memory and battery" },
  { slug: "tablets", title: "Tablets", copy: "Display, performance and portability" },
  { slug: "laptops", title: "Laptops", copy: "Processors, graphics and configurations" }
] as const;

export default function BrowsePage() {
  return <section className={`page-shell section ${styles.browser}`}><header className={styles.heading}><div><span className={styles.eyebrow}>Catalog</span><h1>Choose a device category</h1><p>Each category has its own filters and results.</p></div></header>
    <div className={styles.categories}>{categories.map((category) => {
      const devices = devicesForCategory(category.slug);
      const featured = devices.find((device) => device.imageId) ?? devices[0];
      return <Link className={styles.categoryCard} href={`/browse/${category.slug}`} key={category.slug}>{featured && <CatalogProductImage device={featured} sizes="(max-width: 650px) 90vw, 30vw" />}<div className={styles.categoryCardBody}><span>{devices.length} research records</span><strong>{category.title}</strong><p>{category.copy}</p><b>Browse {category.title.toLowerCase()} <span aria-hidden="true">→</span></b></div></Link>;
    })}</div>
  </section>;
}
