"use client";

/**
 * ===================================
 * MOBILE TAB BAR
 * ===================================
 *
 * Purpose:
 * Provides the fixed bottom navigation for phone-sized screens.
 *
 * Why a separate component:
 * - Desktop navigation stays in the header.
 * - Mobile needs larger touch targets and a fixed thumb-friendly bar.
 */
import type { Route } from "next";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { GitCompareArrows, Heart, House, LayoutDashboard } from "lucide-react";

import styles from "./MobileTabBar.module.css";

const tabs = [
  { href: "/", label: "Home", icon: House },
  { href: "/browse", label: "Browse", icon: LayoutDashboard },
  { href: "/compare", label: "Compare", icon: GitCompareArrows },
  { href: "/favorites", label: "Saved", icon: Heart }
] satisfies Array<{ href: Route; label: string; icon: typeof House }>;

/* Marks a tab active on exact matches and nested route paths. */
function isActivePath(pathname: string, href: Route) {
  if (href === "/") {
    return pathname === "/";
  }

  return pathname === href || pathname.startsWith(`${href}/`);
}

export function MobileTabBar() {
  const pathname = usePathname();

  return (
    /* Only visible on smaller screens through the CSS module. */
    <nav className={`mobile-tabbar ${styles.scope}`} aria-label="Mobile navigation">
      {tabs.map((tab) => {
        const Icon = tab.icon;
        const active = isActivePath(pathname, tab.href);

        return (
          <Link key={tab.href} href={tab.href} className={`mobile-tablink ${active ? "is-active" : ""}`.trim()}>
            <Icon size={16} />
            <span>{tab.label}</span>
          </Link>
        );
      })}
    </nav>
  );
}
