import { useEffect, useState } from "react";
import SectionHeading from "../components/SectionHeading";
import { fetchModelMetrics } from "../lib/api";

const MODEL_BLOCKS = [
  {
    title: "What is now actually trained",
    body: "The app now uses trained decision-tree models for score prediction, summary band prediction, and starting-plate generation.",
  },
  {
    title: "What the model learns from",
    body: "The current training set is a bootstrap dataset generated from the nutrition logic already built into the project. That means the model is real and trained, but it is not yet trained on real user outcomes.",
  },
  {
    title: "Why this is still useful",
    body: "This gives the project a real ML pipeline: dataset generation, train/test split, saved artifacts, inference at runtime, and measurable evaluation before we collect live data later.",
  },
];

const NEXT_STEPS = [
  "Store real survey submissions and accepted plate fixes in a database.",
  "Create labels from user follow-up outcomes instead of only rule-generated targets.",
  "Retrain periodically and compare model outputs against the rule fallback.",
  "Keep safety rules as the final guardrail even after training on real data.",
];

export default function ModelInsightsSection() {
  const [metrics, setMetrics] = useState(null);
  const [loadError, setLoadError] = useState("");

  useEffect(() => {
    let cancelled = false;

    async function loadMetrics() {
      try {
        const data = await fetchModelMetrics();
        if (!cancelled) {
          setMetrics(data);
        }
      } catch {
        if (!cancelled) {
          setLoadError("Model metrics are not available yet.");
        }
      }
    }

    loadMetrics();
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <section className="model-page">
      <SectionHeading
        eyebrow="Model analysis"
        title="Training, results, and testing of the nutrition ML model."
        body="This page now reflects the real trained model used by the app, including what was trained, how it was evaluated, and where the pipeline should go next."
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
          <h3>Measured results</h3>
          {metrics ? (
            <ul>
              <li>Model: {metrics.model_name}</li>
              <li>Training source: {metrics.training_source}</li>
              <li>Samples used: {metrics.sample_count}</li>
              <li>Score MAE: {metrics.score_mae}</li>
              <li>Score R2: {metrics.score_r2}</li>
              <li>Hydration band accuracy: {metrics.hydration_accuracy}</li>
              <li>Meal rhythm accuracy: {metrics.meal_rhythm_accuracy}</li>
              <li>Variety accuracy: {metrics.variety_accuracy}</li>
              <li>Plate base accuracy: {metrics.plate_accuracy.base}</li>
              <li>Plate protein accuracy: {metrics.plate_accuracy.protein}</li>
              <li>Plate vegetable accuracy: {metrics.plate_accuracy.vegetable}</li>
              <li>Plate side accuracy: {metrics.plate_accuracy.side}</li>
            </ul>
          ) : (
            <p>{loadError || "Loading model metrics..."}</p>
          )}
        </article>

        <article className="guidance-card">
          <h3>Testing focus</h3>
          <ul>
            <li>Verify survey inputs map cleanly to a predicted score and a generated starting plate.</li>
            <li>Compare ML outputs with the rule fallback for edge cases and invalid patterns.</li>
            <li>Check that the fixed plate still uses only foods available in the planner options.</li>
            <li>Re-run train/test evaluation whenever the survey schema or allowed plate items change.</li>
          </ul>
        </article>
      </div>

      <article className="model-wide-card">
        <h3>Training log</h3>
        {metrics ? (
          <ol className="model-log-list">
            {metrics.training_log.map((line) => (
              <li key={line}>{line}</li>
            ))}
          </ol>
        ) : (
          <p>{loadError || "Training log will appear once the metrics load."}</p>
        )}
      </article>

      <article className="model-wide-card">
        <h3>What still needs to happen for a stronger ML version</h3>
        <ul>
          {NEXT_STEPS.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </article>
    </section>
  );
}
