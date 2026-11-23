"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { catalogDevices } from "@/lib/catalog/data";
import { CatalogSaveButton, readSavedVariants } from "./CatalogSaveButton";
import styles from "./catalog.module.css";

export function CatalogFavorites() {
  const [saved, setSaved] = useState<string[]>([]);
  useEffect(() => {
    const refresh = () => setSaved(readSavedVariants());
    refresh(); window.addEventListener("deviceiq:saved", refresh);
    return () => window.removeEventListener("deviceiq:saved", refresh);
  }, []);
  const rows = catalogDevices.flatMap((device) => device.variants.map((variant) => ({ device, variant }))).filter(({ variant }) => saved.includes(variant.id));
  return <section className="page-shell section"><header className={styles.heading}><div><span className={styles.eyebrow}>Saved</span><h1>Saved configurations</h1><p>Saved on this browser for quick reference.</p></div></header>{rows.length ? <div className={styles.grid}>{rows.map(({ device, variant }) => <article className={styles.card} key={variant.id}><div className={styles.cardTop}><span className={styles.category}>{device.category.slice(0, -1)}</span><CatalogSaveButton variantId={variant.id} /></div><h2>{device.brand} {device.model}</h2><p className={styles.variant}>{variant.label}</p><Link className="button-secondary" href={`/devices/${device.category}/${device.id}`}>View specifications</Link></article>)}</div> : <div className={styles.empty}><h2>No saved configurations</h2><p>Save a configuration while browsing to find it here.</p><Link className="button-secondary" href="/browse">Choose a category</Link></div>}</section>;
}
