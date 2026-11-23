import { CatalogCompare } from "@/components/catalog/CatalogCompare";
import type { DeviceCategory } from "@/lib/catalog/types";
import { catalogRows } from "@/lib/catalog/data";

export default async function ComparePage({ searchParams }: { searchParams: Promise<{ category?: string; first?: string }> }) {
  const { category: requestedCategory, first: requestedFirst } = await searchParams;
  const category: DeviceCategory = requestedCategory === "smartphones" || requestedCategory === "laptops" ? requestedCategory : "tablets";
  const first = catalogRows(category).some((row) => row.variant.id === requestedFirst) ? requestedFirst : "";
  return <CatalogCompare key={`${category}:${first}`} initialCategory={category} initialFirst={first} />;
}
