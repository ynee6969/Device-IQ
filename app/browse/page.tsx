import Link from "next/link";
import { catalogRows } from "@/lib/catalog/data";
import styles from "@/components/catalog/catalog.module.css";

const categories = [
  { slug: "smartphones", title: "Smartphones", copy: "Explore chipset, memory, cameras and battery." },
  { slug: "tablets", title: "Tablets", copy: "Explore display, chipset, battery, cameras and connectivity." },
  { slug: "laptops", title: "Laptops", copy: "Explore exact configurations, processors, memory and prices." }
] as const;

export default function BrowsePage() {
  return <section className={`page-shell section ${styles.browser}`}><header className={styles.heading}><div><span className={styles.eyebrow}>Catalog</span><h1>Choose a device category</h1><p>Each category has its own filters and results.</p></div></header>
    <div className={styles.categories}>{categories.map((category) => <Link className={styles.categoryCard} href={`/browse/${category.slug}`} key={category.slug}><strong>{category.title}</strong><span>{category.copy}</span><span>{catalogRows(category.slug).length} recorded configurations</span></Link>)}</div>
  </section>;
}
