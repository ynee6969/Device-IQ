"use client";

/**
 * ===================================
 * HEADER AUTH CONTROLS
 * ===================================
 *
 * Purpose:
 * Handles the right side of the header for both guests and signed-in users.
 *
 * Responsibilities:
 * - Show login/signup for guests.
 * - Show account actions for authenticated users.
 * - Collapse those actions into a centered mobile sheet on small screens.
 */
import Link from "next/link";
import { LoaderCircle, LogIn, LogOut, Menu, UserPlus, X } from "lucide-react";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { signOut, useSession } from "next-auth/react";

import styles from "./HeaderAuthControls.module.css";

export function HeaderAuthControls() {
  const pathname = usePathname();
  const { data: session, status } = useSession();
  /* Local state controls the mobile action sheet. */
  const [mobileOpen, setMobileOpen] = useState(false);

  /* Close the sheet whenever navigation or session state changes
     so the overlay never lingers on the wrong page. */
  useEffect(() => {
    setMobileOpen(false);
  }, [pathname, status]);

  function closeMobileSheet() {
    setMobileOpen(false);
  }

  async function handleSignOut() {
    closeMobileSheet();
    await signOut({ callbackUrl: "/" });
  }

  return (
    <>
      {/* Desktop action group stays inline with the main header layout. */}
      <div className={`header-auth-desktop ${styles.desktop}`}>
        {status === "loading" ? (
          <span className="chip muted-chip">
            <LoaderCircle size={14} className="spin" />
            <span>Loading</span>
          </span>
        ) : status === "authenticated" ? (
          <div className="header-auth-group">
            <button
              type="button"
              className="button-ghost header-auth-button"
              onClick={() => void signOut({ callbackUrl: "/" })}
            >
              <LogOut size={16} />
              <span>Sign out</span>
            </button>
          </div>
        ) : (
          <div className="header-auth-group">
            <Link href="/login" className="button-ghost header-auth-button">
              <span>Log in</span>
            </Link>
            <Link href="/signup" className="button header-auth-button">
              <span>Sign up</span>
            </Link>
          </div>
        )}
      </div>

      {/* Mobile gets a single compact trigger instead of wide action buttons. */}
      <div className={`header-auth-mobile ${styles.mobile}`}>
        <button
          type="button"
          className="button-secondary header-mobile-trigger"
          onClick={() => setMobileOpen(true)}
          aria-label="Open account actions"
        >
          {status === "loading" ? <LoaderCircle size={17} className="spin" /> : <Menu size={18} />}
        </button>
      </div>

      {/* Mobile action sheet: centered overlay that keeps menu content visible on short screens. */}
      {mobileOpen ? (
        <div
          className={`sheet-overlay header-account-overlay ${styles.overlay}`}
          role="presentation"
          onClick={closeMobileSheet}
        >
          <div
            className={`sheet-panel header-account-sheet ${styles.panel}`}
            role="dialog"
            aria-modal="true"
            aria-label="Account actions"
            onClick={(event) => event.stopPropagation()}
          >
            <div className="sheet-header header-account-sheet-header">
              <div className="header-account-sheet-copy">
                <strong>{status === "authenticated" ? "Your account" : "Browsing mode"}</strong>
                <p className="muted">
                  {status === "authenticated"
                    ? `Signed in as ${session?.user?.name ?? session?.user?.email ?? "your account"}.`
                    : "Browse without an account, or sign in to manage your account."}
                </p>
              </div>

              <button type="button" className="button-ghost header-account-close" onClick={closeMobileSheet}>
                <X size={16} />
              </button>
            </div>

            {/* Authenticated and guest actions share the same layout shell for consistency. */}
            {status === "authenticated" ? (
              <div className="header-account-actions">
                <button type="button" className="button-ghost header-account-link" onClick={() => void handleSignOut()}>
                  <LogOut size={16} />
                  <span>Sign out</span>
                </button>
              </div>
            ) : (
              <div className="header-account-actions">
                <Link href="/login" className="button-secondary header-account-link" onClick={closeMobileSheet}>
                  <LogIn size={16} />
                  <span>Log in</span>
                </Link>
                <Link href="/signup" className="button header-account-link" onClick={closeMobileSheet}>
                  <UserPlus size={16} />
                  <span>Sign up</span>
                </Link>
              </div>
            )}
          </div>
        </div>
      ) : null}
    </>
  );
}
