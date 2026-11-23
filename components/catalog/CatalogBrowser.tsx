"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import type { CatalogRow, DeviceCategory } from "@/lib/catalog/types";
import { fieldOptions, filterDefinitions, filterRows, pageRows, sortRows, type CatalogSort, type FilterDefinition, type FilterSelections } from "@/lib/catalog/filtering";
import { CatalogCard } from "./CatalogCard";
import styles from "./catalog.module.css";

const categoryLabels: Record<DeviceCategory, string> = { smartphones: "Smartphones", tablets: "Tablets", laptops: "Laptops" };
const groups = ["Basics", "Price and condition", "Performance", "Display", "Camera and video", "Battery and portability", "Connectivity and compatibility"];

function FilterControl({ definition, rows, selections, setSelections }: { definition: FilterDefinition; rows: CatalogRow[]; selections: FilterSelections; setSelections: React.Dispatch<React.SetStateAction<FilterSelections>> }) {
  const id = `${definition.key}:${definition.kind}`;
  const options = fieldOptions(rows, definition.key);
  const [query, setQuery] = useState("");
  const current = selections[id];
  if (!options.length) return null;
  if (definition.kind !== "multi") {
    const thresholds = options.map(Number).filter(Number.isFinite).sort((a, b) => a - b);
    if (!thresholds.length) return null;
    return <label className={styles.field}>
      <span>{definition.label} {definition.unit ? `(${definition.unit})` : ""}</span>
      <select className="select" value={typeof current === "number" ? current : ""} onChange={(event) => setSelections((previous) => ({ ...previous, [id]: event.target.value ? Number(event.target.value) : undefined }))}>
        <option value="">Any verified value</option>
        {thresholds.map((value) => <option key={value} value={value}>{value.toLocaleString("en-PH")}{definition.unit ? ` ${definition.unit}` : ""}{definition.kind === "min" ? " or more" : " or less"}</option>)}
      </select>
    </label>;
  }
  const selected = Array.isArray(current) ? current : [];
  const visible = options.filter((option) => option.toLowerCase().includes(query.toLowerCase()));
  return <fieldset className={styles.choiceField}>
    <legend>{definition.label}</legend>
    {definition.searchable && <input className={styles.search} type="search" aria-label={`Search ${definition.label}`} placeholder={`Search ${definition.label.toLowerCase()}`} value={query} onChange={(event) => setQuery(event.target.value)} />}
    <div className={styles.options}>
      {visible.map((option) => <label key={option} className={styles.check}><input type="checkbox" checked={selected.includes(option)} onChange={(event) => setSelections((previous) => {
        const values = Array.isArray(previous[id]) ? previous[id] as string[] : [];
        return { ...previous, [id]: event.target.checked ? [...values, option] : values.filter((value) => value !== option) };
      })} /><span>{option === "new" ? "New" : option === "used" ? "Used" : option}</span></label>)}
      {visible.length === 0 && <span className={styles.hint}>No recorded options match that search.</span>}
    </div>
  </fieldset>;
}

export function CatalogBrowser({ category, rows }: { category: DeviceCategory; rows: CatalogRow[] }) {
  const definitions = useMemo(() => filterDefinitions(category), [category]);
  const [selections, setSelections] = useState<FilterSelections>({});
  const [search, setSearch] = useState("");
  const [sort, setSort] = useState<CatalogSort>(category === "laptops" ? "price_asc" : "name_asc");
  const [page, setPage] = useState(0);
  const [additional, setAdditional] = useState(false);
  const [filtersOpen, setFiltersOpen] = useState(false);
  const matched = useMemo(() => {
    const term = search.trim().toLowerCase();
    const searched = term ? rows.filter(({ device, variant }) => `${device.brand} ${device.model} ${variant.label}`.toLowerCase().includes(term)) : rows;
    return sortRows(filterRows(searched, definitions, selections), sort);
  }, [rows, definitions, selections, search, sort]);
  const visible = pageRows(matched, page);
  const activeCount = Object.values(selections).filter((value) => Array.isArray(value) ? value.length : value !== undefined).length + Number(Boolean(search.trim()));
  const updateSelections: React.Dispatch<React.SetStateAction<FilterSelections>> = (action) => {
    setPage(0);
    setSelections(action);
  };
  const groupsWithValues = groups.map((group) => ({ group, controls: definitions.filter((definition) => definition.group === group && fieldOptions(rows, definition.key).length > 0 && (!definition.additional || additional)) })).filter(({ controls }) => controls.length);

  return <div className={`page-shell section ${styles.browser}`}>
    <nav className={styles.breadcrumb} aria-label="Breadcrumb"><Link href="/browse">Choose a category</Link><span>/</span><span>{categoryLabels[category]}</span></nav>
    <header className={styles.heading}><div><span className={styles.eyebrow}>Browse</span><h1>{categoryLabels[category]}</h1><p>Explore models, narrow your options, and compare the details.</p></div><span className={styles.count}>{rows.length} {rows.length === 1 ? "model" : "models"}</span></header>
    <button className={`button-secondary ${styles.mobileFiltersToggle}`} type="button" aria-expanded={filtersOpen} aria-controls="catalog-filters" onClick={() => setFiltersOpen((value) => !value)}>{filtersOpen ? "Hide filters" : `Show filters${activeCount ? ` (${activeCount})` : ""}`}</button>
    <div className={styles.layout}>
      <aside id="catalog-filters" className={`${styles.filters} ${filtersOpen ? styles.filtersOpen : ""}`} aria-label="Catalog filters">
        <div className={styles.filterHeader}><h2>Filters</h2><button type="button" onClick={() => { setSelections({}); setSearch(""); setPage(0); }} disabled={!activeCount}>Clear all</button></div>
        <label className={styles.field}><span>Search model or configuration</span><input className={styles.search} type="search" value={search} onChange={(event) => { setSearch(event.target.value); setPage(0); }} placeholder="Search catalog" /></label>
        {groupsWithValues.map(({ group, controls }) => <section className={styles.filterGroup} key={group}><h3>{group}</h3>{controls.map((definition) => <FilterControl key={`${definition.key}:${definition.kind}`} definition={definition} rows={rows} selections={selections} setSelections={updateSelections} />)}</section>)}
        {rows.length > 0 && <button className={styles.additional} type="button" aria-expanded={additional} onClick={() => setAdditional((value) => !value)}>{additional ? "Hide additional filters" : "Additional filters"}</button>}
        {rows.length > 0 && <p className={styles.hint}>Different fields narrow results together. Select several options within one field to include any of them.</p>}
      </aside>
      <section className={styles.results} aria-label="Catalog results">
        <div className={styles.toolbar}><p aria-live="polite">{matched.length} {matched.length === 1 ? "match" : "matches"}{activeCount ? ` · ${activeCount} active filters` : ""}</p><label>Sort by <select className="select" value={sort} onChange={(event) => { setSort(event.target.value as CatalogSort); setPage(0); }}><option value="name_asc">Name A–Z{category !== "laptops" ? " (default)" : ""}</option><option value="name_desc">Name Z–A</option>{rows.some((row) => row.variant.pricePhp !== null) && <><option value="price_asc">Price: low to high{category === "laptops" ? " (default)" : ""}</option><option value="price_desc">Price: high to low</option></>}{rows.some((row) => typeof row.variant.specs.ramGb === "number") && <option value="ram_desc">RAM: high to low</option>}{rows.some((row) => row.device.releaseDate) && <option value="release_desc">Release: newest first</option>}</select></label></div>
        {visible.length ? <div className={styles.grid}>{visible.map((row, index) => <CatalogCard row={row} priority={index < 2} key={row.variant.id} />)}</div> : <div className={styles.empty}><h2>No matching configurations</h2><p>{rows.length ? "Try removing a filter or choosing a different value. Your selections will stay in place until you change them." : "No eligible records are available in this category yet."}</p>{activeCount > 0 && <button className="button-secondary" type="button" onClick={() => { setSelections({}); setSearch(""); setPage(0); }}>Clear filters</button>}</div>}
        {matched.length > 10 && <nav className={styles.pagination} aria-label="Result pages"><button className="button-secondary" type="button" disabled={page === 0} onClick={() => setPage((value) => value - 1)}>Previous</button><span>Page {page + 1} of {Math.ceil(matched.length / 10)}</span><button className="button-secondary" type="button" disabled={(page + 1) * 10 >= matched.length} onClick={() => setPage((value) => value + 1)}>Next</button></nav>}
      </section>
    </div>
  </div>;
}
