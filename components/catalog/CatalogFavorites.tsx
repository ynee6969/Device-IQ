"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { catalogDevices } from "@/lib/catalog/data";
import { readSavedVariants } from "./CatalogSaveButton";
import { CatalogCard } from "./CatalogCard";
import styles from "./catalog.module.css";

export function CatalogFavorites() {
  const [saved, setSaved] = useState<string[]>([]);
  useEffect(() => {
    const refresh = () => setSaved(readSavedVariants());
    refresh(); window.addEventListener("deviceiq:saved", refresh);
    return () => window.removeEventListener("deviceiq:saved", refresh);
  }, []);
  const rows = catalogDevices.flatMap((device) => device.variants.map((variant) => ({ device, variant }))).filter(({ variant }) => saved.includes(variant.id));
  return <section className="page-shell section"><header className={styles.heading}><div><span className={styles.eyebrow}>Saved</span><h1>Saved configurations</h1><p>Saved on this browser for quick reference.</p></div></header>{rows.length ? <div className={styles.grid}>{rows.map((row) => <CatalogCard row={row} key={row.variant.id} />)}</div> : <div className={styles.empty}><h2>No saved configurations</h2><p>Save a configuration while browsing to find it here.</p><Link className="button-secondary" href="/browse">Choose a category</Link></div>}</section>;
}
