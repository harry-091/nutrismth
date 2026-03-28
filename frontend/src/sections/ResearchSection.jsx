import SectionHeading from "../components/SectionHeading";

export default function ResearchSection({ sections }) {
  return (
    <section className="story-section" id="research">
      <SectionHeading
        eyebrow="Research"
        title="The project focuses on hydration, meal quality, and practical habit change."
        body="These sections summarize the nutrition themes that shape the survey and recommendations."
      />

      <div className="story-grid">
        {sections.map((section) => (
          <article key={section.slug} className="story-card">
            <p className="eyebrow">{section.eyebrow}</p>
            <h3>{section.title}</h3>
            <p>{section.body}</p>
            <div className="story-highlights">
              {section.highlights.map((highlight) => (
                <div key={`${section.slug}-${highlight.label}`}>
                  <span>{highlight.label}</span>
                  <strong>{highlight.value}</strong>
                  <p>{highlight.detail}</p>
                </div>
              ))}
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
