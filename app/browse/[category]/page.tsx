import { notFound } from "next/navigation";
import { CatalogBrowser } from "@/components/catalog/CatalogBrowser";
import { catalogRows } from "@/lib/catalog/data";
import type { DeviceCategory } from "@/lib/catalog/types";

export default async function CategoryPage({ params }: { params: Promise<{ category: string }> }) {
  const { category } = await params;
  if (!["smartphones", "tablets", "laptops"].includes(category)) notFound();
  return <CatalogBrowser category={category as DeviceCategory} rows={catalogRows(category)} />;
}
