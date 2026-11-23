import { site } from "@/lib/site";

export default function ContactPage() {
  return <section className="section"><div className="page-shell stack">
    <h1 className="section-title">Contact DeviceIQ</h1>
    <p className="section-copy">To report a specification or price correction, include the model, configuration and source link.</p>
    <p><a className="button-secondary" href={`mailto:${site.email}`}>Email {site.email}</a></p>
  </div></section>;
}
