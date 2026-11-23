"use client";

import Link from "next/link";
import { useState } from "react";
import { catalogRows } from "@/lib/catalog/data";
import type { DeviceCategory, SpecKey } from "@/lib/catalog/types";
import styles from "./catalog.module.css";

const fields: [SpecKey, string][] = [["laptopType", "Type"], ["os", "Operating system"], ["chipset", "Chipset"], ["cpu", "CPU"], ["gpu", "GPU"], ["ramGb", "RAM (GB)"], ["storageGb", "Storage (GB)"], ["displayInches", "Display (in)"], ["displayType", "Display type"], ["resolution", "Resolution"], ["refreshHz", "Refresh rate (Hz)"], ["rearCameraMp", "Rear camera (MP)"], ["frontCameraMp", "Front camera (MP)"], ["batteryMah", "Battery (mAh)"], ["batteryWh", "Battery (Wh)"], ["weightG", "Weight (g)"], ["wifi", "Wi-Fi"]];

export function CatalogCompare({ initialCategory = "tablets", initialFirst = "" }: { initialCategory?: DeviceCategory; initialFirst?: string }) {
  const [category, setCategory] = useState<DeviceCategory>(initialCategory);
  const [left, setLeft] = useState(initialFirst);
  const [right, setRight] = useState("");
  const rows = catalogRows(category);
  const leftRow = rows.find((row) => row.variant.id === left);
  const rightRow = rows.find((row) => row.variant.id === right);
  return <div className="page-shell section"><header className={styles.heading}><div><span className={styles.eyebrow}>Compare</span><h1>Compare configurations</h1><p>Choose two records from the same device category.</p></div></header>
    <section className={styles.comparePanel}><div className={styles.compareSelectors}><label className={styles.field}><span>Device category</span><select className="select" value={category} onChange={(event) => { setCategory(event.target.value as DeviceCategory); setLeft(""); setRight(""); }}><option value="smartphones">Smartphones</option><option value="tablets">Tablets</option><option value="laptops">Laptops</option></select></label><label className={styles.field}><span>First configuration</span><select className="select" value={left} onChange={(event) => setLeft(event.target.value)}><option value="">Select a device</option>{rows.map(({ device, variant }) => <option key={variant.id} value={variant.id}>{device.brand} {device.model} · {variant.label}</option>)}</select></label><label className={styles.field}><span>Second configuration</span><select className="select" value={right} onChange={(event) => setRight(event.target.value)}><option value="">Select a device</option>{rows.filter(({ variant }) => variant.id !== left).map(({ device, variant }) => <option key={variant.id} value={variant.id}>{device.brand} {device.model} · {variant.label}</option>)}</select></label></div>
    {leftRow && rightRow && left !== right && <table className={styles.compareTable}><thead><tr><th>Specification</th><th><Link href={`/devices/${category}/${leftRow.device.id}`}>{leftRow.device.brand} {leftRow.device.model}</Link></th><th><Link href={`/devices/${category}/${rightRow.device.id}`}>{rightRow.device.brand} {rightRow.device.model}</Link></th></tr></thead><tbody><tr><th>Configuration</th><td>{leftRow.variant.label}</td><td>{rightRow.variant.label}</td></tr><tr><th>Listed price</th><td>{leftRow.variant.pricePhp === null ? "Not verified" : `₱${leftRow.variant.pricePhp.toLocaleString("en-PH")}`}</td><td>{rightRow.variant.pricePhp === null ? "Not verified" : `₱${rightRow.variant.pricePhp.toLocaleString("en-PH")}`}</td></tr>{fields.filter(([key]) => leftRow.variant.specs[key] !== undefined || rightRow.variant.specs[key] !== undefined).map(([key, label]) => <tr key={key}><th>{label}</th><td>{String(leftRow.variant.specs[key] ?? "Not verified")}</td><td>{String(rightRow.variant.specs[key] ?? "Not verified")}</td></tr>)}</tbody></table>}
    {left && right && left === right && <p role="alert" className={styles.sourceLine}>Choose two different configurations.</p>}
    </section>
  </div>;
}
