import SectionHeading from "../components/SectionHeading";

const MODEL_BLOCKS = [
  {
    title: "Current model approach",
    body: "The current system uses a rule-based scoring model. Inputs like hydration, meal pattern, sugary drinks, activity level, and plate composition are converted into weighted decisions and structured outputs.",
  },
  {
    title: "Features used",
    body: "Survey fields such as age group, meal frequency, hydration behavior, produce intake, protein sources, sleep pattern, exercise frequency, and plate selections act as the feature set for analysis.",
  },
  {
    title: "Expected output",
    body: "The app returns a nutrition score, risk indicators, hydration guidance, plate advice, smart swaps, and a corrected meal plate if the user uses the planner.",
  },
];

const RESULTS = [
  "Users with lower water intake and higher sugary drink frequency are pushed into higher-risk hydration bands.",
  "Meal patterns with more vegetables, dal, curd, and balanced lunch combinations receive stronger nutrition scores.",
  "The plate planner improves a meal by replacing refined or low-quality picks with better choices from the same allowed menu.",
];

const TEST_CASES = [
  "Low hydration + irregular meals + packaged snacks should reduce the score noticeably.",
  "Balanced meals + regular produce + moderate activity should improve the score.",
  "White rice + soft drink + fries should trigger at least one replacement in the plate planner.",
  "A plate that is already balanced should return few or no adjustments.",
];

const NEXT_STEPS = [
  "Store survey and plate submissions in a database.",
  "Build a labeled dataset from user inputs and accepted recommendations.",
  "Train a baseline classifier or regressor for score and risk prediction.",
  "Keep business rules as a safety layer even after adding ML inference.",
];

export default function ModelInsightsSection() {
  return (
    <section className="model-page">
      <SectionHeading
        eyebrow="Model analysis"
        title="Analysis, results, and testing of the nutrition model."
        body="This page explains how the current scoring system behaves, what inputs it uses, what outputs it produces, and how it can evolve into a real machine learning pipeline."
      />

      <div className="model-grid">
        {MODEL_BLOCKS.map((block) => (
          <article key={block.title} className="model-card">
            <h3>{block.title}</h3>
            <p>{block.body}</p>
          </article>
        ))}
      </div>

      <div className="guidance-grid model-guidance-grid">
        <article className="guidance-card">
          <h3>Observed results</h3>
          <ul>
            {RESULTS.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </article>

        <article className="guidance-card">
          <h3>Testing focus</h3>
          <ul>
            {TEST_CASES.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </article>
      </div>

      <article className="model-wide-card">
        <h3>How a real ML version would be built</h3>
        <ul>
          {NEXT_STEPS.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </article>
    </section>
  );
}
