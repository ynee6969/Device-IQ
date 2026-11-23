import Image from "next/image";
import Link from "next/link";
import { HeroSection } from "@/components/marketing/hero-section";
import { curatedGallery } from "@/lib/data/seed-phones";
import { getLocalPhoneImageUrl } from "@/lib/services/phone-images";
import { formatPhp, slugify } from "@/lib/utils/format";
import { getPhoneDisplayName } from "@/lib/utils/phone-presentation";
import styles from "./page.module.css";

export default function HomePage() {
  return <div className={`page-shell section ${styles.home}`}>
    <HeroSection />
    <section aria-labelledby="examples"><div className={styles.heading}>
      <div><h2 id="examples">From the smartphone catalog</h2><p className="muted">Illustrative prices and specifications</p></div>
      <Link href="/dashboard">Browse all phones</Link></div>
      <div className={styles.grid}>{curatedGallery.slice(0, 3).map(phone => {
        const slug = slugify(phone.brand + "-" + phone.model);
        const image = getLocalPhoneImageUrl(slug);
        return <Link href={`/phones/${slug}`} key={slug} className={`glass-panel ${styles.phone}`}>
          {image && <Image alt="" src={image} width={110} height={134} />}
          <div><h3>{getPhoneDisplayName(phone.brand, phone.model)}</h3>
          <p>{formatPhp(phone.price)} · {phone.battery.toLocaleString("en-PH")} mAh</p></div></Link>;
      })}</div>
    </section>
  </div>;
}
