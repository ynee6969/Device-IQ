"use client";

import { useEffect, useState } from "react";

const KEY = "deviceiq:saved-variants";
export function readSavedVariants(): string[] {
  if (typeof window === "undefined") return [];
  try { const value = JSON.parse(localStorage.getItem(KEY) ?? "[]"); return Array.isArray(value) ? value.filter((item): item is string => typeof item === "string") : []; }
  catch { return []; }
}

export function CatalogSaveButton({ variantId }: { variantId: string }) {
  const [saved, setSaved] = useState(false);
  useEffect(() => { setSaved(readSavedVariants().includes(variantId)); }, [variantId]);
  return <button type="button" aria-pressed={saved} aria-label={saved ? "Remove from saved" : "Save configuration"} onClick={() => {
    const next = saved ? readSavedVariants().filter((id) => id !== variantId) : [...new Set([...readSavedVariants(), variantId])];
    localStorage.setItem(KEY, JSON.stringify(next)); setSaved(!saved); window.dispatchEvent(new Event("deviceiq:saved"));
  }}>{saved ? "Saved" : "Save"}</button>;
}
