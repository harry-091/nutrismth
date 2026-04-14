import SectionHeading from "../components/SectionHeading";
import { useState } from "react";

const OPTIONS = {
  base: [
    "brown rice",
    "multigrain roti",
    "millet khichdi",
    "quinoa pulao",
    "oats chilla",
    "idli",
    "poha",
    "sweet potato bowl",
    "white rice",
    "butter naan",
    "instant noodles",
    "creamy pasta",
  ],
  protein: [
    "dal tadka",
    "rajma masala",
    "chickpea curry",
    "paneer tikka",
    "egg bhurji",
    "grilled chicken",
    "fish curry",
    "tofu stir-fry",
    "soy chunk masala",
    "hung curd dip",
    "fried chicken",
    "creamy paneer",
  ],
  cooked_veg: [
    "bhindi sabzi",
    "lauki sabzi",
    "spinach corn",
    "cabbage peas",
    "roasted broccoli",
    "mixed veg stir-fry",
    "pumpkin sabzi",
    "mushroom pepper saute",
    "potato fries",
    "crispy corn",
    "none",
  ],
  fresh_side: [
    "cucumber salad",
    "kachumber salad",
    "fruit bowl",
    "sprout chaat",
    "carrot sticks",
    "tomato onion salad",
    "mint yogurt salad",
    "nachos",
    "cream biscuit",
    "none",
  ],
  drink: [
    "water",
    "buttermilk",
    "lemon water",
    "coconut water",
    "unsweetened chai",
    "plain lassi",
    "sweet soda",
    "packaged juice",
    "milkshake",
  ],
  add_on: [
    "curd bowl",
    "roasted makhana",
    "nuts and seeds",
    "peanut chutney",
    "hummus",
    "pickle",
    "gulab jamun",
    "salted chips",
  ],
};

const CATEGORY_LABELS = {
  base: "Base",
  protein: "Protein",
  cooked_veg: "Cooked Veg",
  fresh_side: "Fresh Side",
  drink: "Drink",
  add_on: "Add-on",
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
          placeholder={`Search ${CATEGORY_LABELS[category].toLowerCase()} options`}
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
  loading,
  data,
  error,
  onNavigate,
  onViewResults,
}) {
  return (
    <section className="plate-planner-page">
      <div className="plate-builder-card">
        <SectionHeading
          eyebrow="Plate planner"
          title="Your survey has already built a balanced plate."
          body="Change any section you want and the plate rating updates live. There is no separate fix step now, because the starting plate is already designed to be a strong option."
        />

        <div className="plate-visual plate-visual-expanded">
          {Object.entries(CATEGORY_LABELS).map(([category, label]) => (
            <div key={category} className={`plate-zone zone-${category}`}>
              <span>{label}</span>
              <strong>{plateForm.items[category]}</strong>
            </div>
          ))}
        </div>

        <div className="plate-config-grid plate-config-grid-expanded">
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
          eyebrow="Live rating"
          title="Your plate score updates with every change."
          body="Body details and meal goal also affect the live rating, so you can tune the plate in a more realistic way."
        />

        <div className="results-summary plate-result-summary">
          <div>
            <span>Plate score</span>
            <strong>{data ? data.score : "--"}</strong>
          </div>
          <div>
            <span>Status</span>
            <strong>{loading ? "Updating..." : "Live"}</strong>
          </div>
          <div>
            <span>Vegetable focus</span>
            <strong>{data ? data.target_split.vegetables : "--"}</strong>
          </div>
          <div>
            <span>Protein focus</span>
            <strong>{data ? data.target_split.protein : "--"}</strong>
          </div>
        </div>

        <div className="plate-profile-form">
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
        </div>

        {error ? <p className="form-error">{error}</p> : null}

        <div className="plate-planner-actions">
          <button type="button" className="button button-secondary" onClick={() => onNavigate("survey")}>
            Back to survey
          </button>
          <button type="button" className="button button-primary" onClick={onViewResults}>
            View full analysis
          </button>
        </div>
      </div>

      <div className="plate-results-card">
        <SectionHeading
          eyebrow="Plate analysis"
          title={data ? "Why your current plate scores this way." : "Your live plate analysis will appear here."}
          body={
            data
              ? data.summary
              : "Once the plate is ready, section-by-section explanations and overall tips will appear here."
          }
        />

        {data ? (
          <>
            <div className="optimized-plate-grid plate-analysis-grid">
              {data.adjustments.map((item) => (
                <article key={`${item.category}-${item.updated}`} className="optimized-plate-item">
                  <span>{item.category.replaceAll("_", " ")}</span>
                  <strong>{item.updated}</strong>
                  <p>{item.reason}</p>
                </article>
              ))}
            </div>

            <div className="guidance-grid">
              <article className="guidance-card">
                <h3>Target structure</h3>
                <ul>
                  <li>{data.target_split.base}</li>
                  <li>{data.target_split.protein}</li>
                  <li>{data.target_split.vegetables}</li>
                  <li>{data.target_split.drink}</li>
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
