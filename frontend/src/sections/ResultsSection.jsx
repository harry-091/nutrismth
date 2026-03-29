import SectionHeading from "../components/SectionHeading";

function GuidanceBlock({ card }) {
  return (
    <article className="guidance-card">
      <h3>{card.title}</h3>
      <p>{card.summary}</p>
      <ul>
        {card.actions.map((action) => (
          <li key={action}>{action}</li>
        ))}
      </ul>
    </article>
  );
}

export default function ResultsSection({ data, onNavigate, onRetakeSurvey }) {
  if (!data) {
    return (
      <section className="results-placeholder">
        <SectionHeading
          eyebrow="Results"
          title="Your results will appear here after the survey."
          body="You’ll get a score, a few priority areas, and practical next steps."
        />
        <button type="button" className="button button-primary" onClick={() => onNavigate("survey")}>
          Go to survey page
        </button>
      </section>
    );
  }

  return (
    <section className="results-section">
      <SectionHeading
        eyebrow="Your nutrition response"
        title="Your current habits and the strongest next steps."
        body={data.confidence_note}
      />

      <div className="results-summary">
        <div>
          <span>Nutrition score</span>
          <strong>{data.score}</strong>
        </div>
        <div>
          <span>Hydration band</span>
          <strong>{data.user_summary.hydration_band}</strong>
        </div>
        <div>
          <span>Meal pattern</span>
          <strong>{data.user_summary.meal_pattern_band}</strong>
        </div>
        <div>
          <span>Variety level</span>
          <strong>{data.user_summary.nutrition_variety_band}</strong>
        </div>
      </div>

      <div className="risk-grid">
        {data.risk_indicators.map((risk) => (
          <article key={risk.title} className={`risk-card risk-${risk.level}`}>
            <span>{risk.level} priority</span>
            <h3>{risk.title}</h3>
            <p>{risk.description}</p>
          </article>
        ))}
      </div>

      <div className="guidance-grid">
        <GuidanceBlock card={data.hydration_recommendation} />
        <GuidanceBlock card={data.plate_guidance} />
        <GuidanceBlock card={data.smart_swaps} />
        <GuidanceBlock card={data.nutrient_education} />
      </div>

      <div className="results-actions">
        <button type="button" className="button button-secondary" onClick={onRetakeSurvey}>
          Retake survey
        </button>
        <button type="button" className="button button-primary" onClick={() => onNavigate("home")}>
          Back home
        </button>
      </div>
    </section>
  );
}
