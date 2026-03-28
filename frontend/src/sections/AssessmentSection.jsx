import SectionHeading from "../components/SectionHeading";

const FIELD_OPTIONS = {
  age_group: ["13-17", "18-25", "26-40", "41-60", "60+"],
  gender: ["female", "male", "non-binary", "prefer_not_to_say"],
  hydration_level: ["low", "medium", "high"],
  meal_pattern: ["irregular", "mixed", "balanced"],
  produce_frequency: ["rarely", "sometimes", "daily"],
  snack_preference: ["packaged", "mixed", "whole_food"],
  activity_level: ["low", "moderate", "high"],
};

function SelectField({ label, name, value, onChange, options }) {
  return (
    <label className="form-field">
      <span>{label}</span>
      <select name={name} value={value} onChange={onChange}>
        {options.map((option) => (
          <option key={option} value={option}>
            {option.replaceAll("_", " ")}
          </option>
        ))}
      </select>
    </label>
  );
}

function NumberField({ label, name, value, onChange, min, max, step }) {
  return (
    <label className="form-field">
      <span>{label}</span>
      <input
        type="number"
        name={name}
        value={value}
        onChange={onChange}
        min={min}
        max={max}
        step={step}
      />
    </label>
  );
}

export default function AssessmentSection({
  form,
  onChange,
  onSubmit,
  loading,
  error,
  step,
  totalSteps,
  onBack,
  onNextStep,
  onNavigate,
}) {
  const stepFields = [
    ["age_group", "gender"],
    ["water_intake_liters", "hydration_level"],
    ["meal_pattern", "produce_frequency"],
    ["snack_preference", "sugary_drinks_per_week", "activity_level"],
  ];

  const fieldMeta = {
    age_group: {
      type: "select",
      label: "Age group",
      options: FIELD_OPTIONS.age_group,
    },
    gender: {
      type: "select",
      label: "Gender",
      options: FIELD_OPTIONS.gender,
    },
    water_intake_liters: {
      type: "number",
      label: "Daily water intake (liters)",
      min: 0.2,
      max: 8,
      step: 0.1,
    },
    hydration_level: {
      type: "select",
      label: "Hydration self-rating",
      options: FIELD_OPTIONS.hydration_level,
    },
    meal_pattern: {
      type: "select",
      label: "Meal pattern",
      options: FIELD_OPTIONS.meal_pattern,
    },
    produce_frequency: {
      type: "select",
      label: "Produce frequency",
      options: FIELD_OPTIONS.produce_frequency,
    },
    snack_preference: {
      type: "select",
      label: "Snack preference",
      options: FIELD_OPTIONS.snack_preference,
    },
    sugary_drinks_per_week: {
      type: "number",
      label: "Sugary drinks per week",
      min: 0,
      max: 35,
      step: 1,
    },
    activity_level: {
      type: "select",
      label: "Activity level",
      options: FIELD_OPTIONS.activity_level,
    },
  };

  const stepTitles = [
    "A few basics about you",
    "Let’s talk hydration",
    "How your meals usually look",
    "Snacks, sweet drinks, and movement",
  ];

  const activeFields = stepFields[step];

  return (
    <section className="assessment-section" id="assessment">
      <div className="assessment-copy">
        <SectionHeading
          eyebrow="Assessment"
          title="A short survey builds your nutrition response step by step."
          body="Move through a few quick sections and submit when everything looks right."
        />
        <div className="survey-progress-card">
          <span>Step {step + 1} of {totalSteps}</span>
          <strong>{stepTitles[step]}</strong>
          <div className="survey-progress-bar">
            <div style={{ width: `${((step + 1) / totalSteps) * 100}%` }} />
          </div>
        </div>
        <ul className="assessment-notes">
          <li>Focused on hydration, meal rhythm, food quality, and activity level.</li>
          <li>Built to keep the inputs short and easy to complete.</li>
          <li>Results are returned as clear recommendation cards.</li>
        </ul>
        <div className="survey-page-links">
          <button type="button" className="button button-secondary" onClick={() => onNavigate("quiz")}>
            Back to game
          </button>
          <button type="button" className="button button-secondary" onClick={() => onNavigate("research")}>
            View research page
          </button>
          <button type="button" className="button button-secondary" onClick={() => onNavigate("plate")}>
            Open plate planner
          </button>
        </div>
      </div>

      <form className="assessment-form" onSubmit={onSubmit}>
        <div className="survey-step-header">
          <span className="eyebrow">Current step</span>
          <h3>{stepTitles[step]}</h3>
        </div>
        <div className="form-grid">
          {activeFields.map((fieldName) => {
            const meta = fieldMeta[fieldName];

            if (meta.type === "select") {
              return (
                <SelectField
                  key={fieldName}
                  label={meta.label}
                  name={fieldName}
                  value={form[fieldName]}
                  onChange={onChange}
                  options={meta.options}
                />
              );
            }

            return (
              <NumberField
                key={fieldName}
                label={meta.label}
                name={fieldName}
                value={form[fieldName]}
                onChange={onChange}
                min={meta.min}
                max={meta.max}
                step={meta.step}
              />
            );
          })}
        </div>

        {error ? <p className="form-error">{error}</p> : null}

        <div className="survey-actions">
          <button
            type="button"
            className="button button-secondary"
            onClick={onBack}
            disabled={step === 0 || loading}
          >
            Back
          </button>
          {step < totalSteps - 1 ? (
            <button
              type="button"
              className="button button-primary"
              onClick={onNextStep}
              disabled={loading}
            >
              Next step
            </button>
          ) : (
            <button className="button button-primary" type="submit" disabled={loading}>
              {loading ? "Generating guidance..." : "See my recommendations"}
            </button>
          )}
        </div>
      </form>
    </section>
  );
}
