import SectionHeading from "../components/SectionHeading";

const PILLARS = [
  {
    title: "Hydration support",
    text: "Convert water intake into timed habits, visible progress, and practical cues that fit a daily routine.",
  },
  {
    title: "Plate balancing",
    text: "Use a visual plate method to make portion balance easier than calorie tracking or rigid dieting.",
  },
  {
    title: "Smarter swaps",
    text: "Recommend whole-grain and whole-food substitutions that feel familiar enough to repeat.",
  },
  {
    title: "Nutrient education",
    text: "Explain the role of protein, fiber, vitamins, and minerals so the product builds understanding along with compliance.",
  },
];

export default function PillarsSection() {
  return (
    <section className="pillars-section">
      <SectionHeading
        eyebrow="Core areas"
        title="Four areas shape the recommendation flow."
      />

      <div className="pillars-grid">
        {PILLARS.map((pillar, index) => (
          <article key={pillar.title} className="pillar-card">
            <span>{String(index + 1).padStart(2, "0")}</span>
            <h3>{pillar.title}</h3>
            <p>{pillar.text}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
