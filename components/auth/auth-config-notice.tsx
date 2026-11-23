/**
 * ===================================
 * AUTH CONFIG NOTICE
 * ===================================
 *
 * Purpose:
 * Shows a friendly setup message when auth secrets are missing in the environment.
 *
 * Why this matters:
 * Instead of crashing the page, the app explains what is missing and gives the user
 * a way back to the public catalog.
 */
import Link from "next/link";

import { authConfigurationMessage } from "@/lib/auth/config";
import styles from "./AuthForm.module.css";

export function AuthConfigNotice() {
  return (
    <div className={`auth-shell ${styles.scope}`}>
      <div className="glass-panel auth-card">
        <span className="section-label">Setup required</span>
        <h1 className="feature-title">Authentication is not configured yet.</h1>
        <p className="section-copy" style={{ maxWidth: "none" }}>
          {authConfigurationMessage}
        </p>
        <p className="muted" style={{ marginBottom: 0 }}>
          Account access will be available after the site administrator configures authentication.
        </p>
        <div className="button-row" style={{ marginTop: 20 }}>
          <Link href="/browse" className="button-secondary">
            Browse devices
          </Link>
        </div>
      </div>
    </div>
  );
}
