import SectionHeading from "../components/SectionHeading";
import { useState } from "react";

const OPTIONS = {
  base: [
    "white rice",
    "brown rice",
    "millet",
    "roti",
    "multigrain roti",
    "quinoa",
    "oats",
    "poha",
    "idli",
    "dosa",
    "upma",
    "noodles",
    "millet noodles",
  ],
  protein: [
    "paneer",
    "dal",
    "rajma",
    "chole",
    "eggs",
    "grilled chicken",
    "fried chicken",
    "fish",
    "tofu",
    "soy chunks",
    "curd",
  ],
  vegetable: [
    "salad",
    "sabzi",
    "mixed vegetables",
    "spinach",
    "broccoli",
    "cucumber",
    "carrot",
    "sauteed vegetables",
    "potato fries",
    "none",
  ],
  side: [
    "fruit",
    "curd",
    "buttermilk",
    "water",
    "nuts and seeds",
    "sprouts",
    "chips",
    "soft drink",
    "pickle",
  ],
};

const CATEGORY_LABELS = {
  base: "Base",
  protein: "Protein",
  vegetable: "Vegetable",
  side: "Side",
};

function ChoiceChips({ category, value, onChange }) {
  const [query, setQuery] = useState("");
  const filteredOptions = OPTIONS[category].filter((option) =>
    option.toLowerCase().includes(query.trim().toLowerCase()),
  );

  return (
    <>
      <label className="plate-search">
        <span>Search</span>
        <input
          type="text"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder={`Search ${category} options`}
        />
      </label>

      <div className="plate-choice-group">
        {filteredOptions.length ? (
          filteredOptions.map((option) => (
            <button
              key={option}
              type="button"
              className={value === option ? "plate-chip active" : "plate-chip"}
              onClick={() => onChange(category, option)}
            >
              {option}
            </button>
          ))
        ) : (
          <p className="plate-empty-state">No matching options.</p>
        )}
      </div>
    </>
  );
}

export default function PlatePlannerSection({
  plateForm,
  onPlateItemChange,
  onProfileChange,
  onSubmit,
  loading,
  data,
  error,
  onNavigate,
}) {
  return (
    <section className="plate-planner-page">
      <div className="plate-builder-card">
        <SectionHeading
          eyebrow="Plate planner"
          title="Review the generated plate and let the app rebalance it."
          body="The survey has already built a starting plate for you. You can still tweak any food choice here before asking for a corrected version with detailed swaps and portion guidance."
        />

        <div className="plate-visual">
          {Object.entries(CATEGORY_LABELS).map(([category, label]) => (
            <div key={category} className={`plate-zone zone-${category}`}>
              <span>{label}</span>
              <strong>{plateForm.items[category]}</strong>
            </div>
          ))}
        </div>

        <div className="plate-config-grid">
          {Object.keys(CATEGORY_LABELS).map((category) => (
            <div key={category} className="plate-config-card">
              <p className="eyebrow">{CATEGORY_LABELS[category]}</p>
              <ChoiceChips
                category={category}
                value={plateForm.items[category]}
                onChange={onPlateItemChange}
              />
            </div>
          ))}
        </div>
      </div>

      <div className="plate-profile-card">
        <SectionHeading
          eyebrow="Your details"
          title="Check the details used to fix the plate."
        />

        <form className="plate-profile-form" onSubmit={onSubmit}>
          <label className="form-field">
            <span>Age group</span>
            <select name="age_group" value={plateForm.profile.age_group} onChange={onProfileChange}>
              <option value="15-18">15-18</option>
              <option value="19-25">19-25</option>
              <option value="26-35">26-35</option>
              <option value="35+">35+</option>
            </select>
          </label>

          <label className="form-field">
            <span>Gender</span>
            <select name="gender" value={plateForm.profile.gender} onChange={onProfileChange}>
              <option value="female">female</option>
              <option value="male">male</option>
            </select>
          </label>

          <label className="form-field">
            <span>Body weight (kg)</span>
            <input
              type="number"
              name="body_weight_kg"
              min="25"
              max="250"
              step="1"
              value={plateForm.profile.body_weight_kg}
              onChange={onProfileChange}
            />
          </label>

          <label className="form-field">
            <span>Activity level</span>
            <select
              name="activity_level"
              value={plateForm.profile.activity_level}
              onChange={onProfileChange}
            >
              <option value="low">low</option>
              <option value="moderate">moderate</option>
              <option value="high">high</option>
            </select>
          </label>

          <label className="form-field">
            <span>Meal goal</span>
            <select name="goal" value={plateForm.profile.goal} onChange={onProfileChange}>
              <option value="balanced">balanced</option>
              <option value="higher_protein">higher protein</option>
              <option value="lighter_meal">lighter meal</option>
              <option value="energy_support">energy support</option>
            </select>
          </label>

          {error ? <p className="form-error">{error}</p> : null}

          <div className="plate-planner-actions">
            <button type="button" className="button button-secondary" onClick={() => onNavigate("survey")}>
              Back to survey
            </button>
            <button type="submit" className="button button-primary" disabled={loading}>
              {loading ? "Fixing plate..." : "Fix my plate"}
            </button>
          </div>
        </form>
      </div>

      <div className="plate-results-card">
        <SectionHeading
          eyebrow="Adjusted plate"
          title={data ? "Your corrected plate is ready." : "Your adjusted plate will appear here."}
          body={
            data
              ? data.summary
              : "After you submit the meal, the app will suggest swaps and a better plate split."
          }
        />

        {data ? (
          <>
            <div className="results-summary plate-result-summary">
              <div>
                <span>Plate score</span>
                <strong>{data.score}</strong>
              </div>
              <div>
                <span>Vegetables</span>
                <strong>{data.target_split.vegetables}</strong>
              </div>
              <div>
                <span>Protein</span>
                <strong>{data.target_split.protein}</strong>
              </div>
              <div>
                <span>Carbs</span>
                <strong>{data.target_split.smart_carbs}</strong>
              </div>
            </div>

            <div className="optimized-plate-grid">
              {data.optimized_plate.map((item) => (
                <article key={`${item.category}-${item.name}`} className="optimized-plate-item">
                  <span>{item.category}</span>
                  <strong>{item.name}</strong>
                </article>
              ))}
            </div>

            <div className="guidance-grid">
              <article className="guidance-card">
                <h3>What changed</h3>
                <ul>
                  {data.adjustments.length ? (
                    data.adjustments.map((item) => (
                      <li key={`${item.category}-${item.updated}`}>
                        {item.original} to {item.updated}: {item.reason}
                      </li>
                    ))
                  ) : (
                    <li>The current plate already fits the selected goal well.</li>
                  )}
                </ul>
              </article>

              <article className="guidance-card">
                <h3>Tips</h3>
                <ul>
                  {data.tips.map((tip) => (
                    <li key={tip}>{tip}</li>
                  ))}
                </ul>
              </article>
            </div>
          </>
        ) : null}
      </div>
    </section>
  );
}
