/**
 * ===================================
 * SITE FOOTER
 * ===================================
 *
 * Purpose:
 * Ends every page with a compact brand reminder and a short product summary.
 *
 * Design choice:
 * The footer stays intentionally small so the app still feels product-focused,
 * especially on catalog-heavy routes like dashboard and compare.
 */
import Link from "next/link";
import { BrandLockup } from "@/components/marketing/brand-lockup";
import styles from "./SiteFooter.module.css";

export function SiteFooter() {
  return (
    <footer className={styles.footer}>
      <div className={styles.inner}>
        <div>
          <BrandLockup subtitle="Browse, compare, and save phones." />
        </div>
        <p className={styles.note}>
          <Link href="/about">Method and sources</Link> · <Link href="/services">Tools</Link> · <Link href="/contact">Contact</Link>
        </p>
      </div>
    </footer>
  );
}
