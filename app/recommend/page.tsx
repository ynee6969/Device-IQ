import { RecommendationWorkspace } from "@/components/recommendation/recommendation-workspace";
import { listPhones } from "@/lib/services/phones";

export const metadata = {
  title: "Smartphone Recommendation"
};

export default async function RecommendPage() {
  const catalog = await listPhones({ take: 1 });

  return (
    <section className="section">
      <div className="page-shell">
        <RecommendationWorkspace brands={catalog.brands} />
      </div>
    </section>
  );
}
