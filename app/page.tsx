import Link from "next/link";
import styles from "@/components/catalog/catalog.module.css";

export default function HomePage() {
  return <div className="page-shell section"><header className={styles.heading}><div><span className={styles.eyebrow}>DeviceIQ</span><h1>Find the details that matter.</h1><p>Browse smartphones, tablets and laptops in separate catalogs. Apply clear filters, inspect configurations and check the sources behind each record.</p><div className="button-row" style={{ marginTop: "1.5rem" }}><Link className="button" href="/browse">Browse devices</Link><Link className="button-secondary" href="/compare">Compare configurations</Link></div></div></header>
    <div className={styles.categories}><Link className={styles.categoryCard} href="/browse/smartphones"><strong>Smartphones</strong><span>10 sourced configurations</span></Link><Link className={styles.categoryCard} href="/browse/tablets"><strong>Tablets</strong><span>10 sourced configurations</span></Link><Link className={styles.categoryCard} href="/browse/laptops"><strong>Laptops</strong><span>10 sourced configurations</span></Link></div>
  </div>;
}
