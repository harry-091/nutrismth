import SectionHeading from "../components/SectionHeading";

const SURVEY_STEPS = [
  {
    title: "Basic profile",
    body: "These answers set the base context for the meal pattern and plate logic.",
    fields: ["age_group", "gender", "diet_type", "activity_level"],
  },
  {
    title: "Daily routine",
    body: "This part captures how often you eat, hydrate, and how balanced your meals feel.",
    fields: [
      "meals_per_day",
      "fruit_veg_frequency",
      "diet_trend",
      "water_intake",
      "post_carb_feeling",
    ],
  },
  {
    title: "Food pattern",
    body: "These questions determine what kind of plate gets generated from your regular habits.",
    fields: ["carb_source", "protein_source", "fat_source", "goal_victory"],
  },
  {
    title: "Meal style",
    body: "Breakfast and dinner patterns help shape the starting plate before it gets fixed.",
    fields: ["breakfast_type", "dinner_type"],
  },
];

const FIELD_META = {
  age_group: {
    label: "Your age",
    options: [
      ["15-18", "15-18"],
      ["19-25", "19-25"],
      ["26-35", "26-35"],
      ["35+", "35+"],
    ],
  },
  gender: {
    label: "Gender",
    options: [
      ["female", "Female"],
      ["male", "Male"],
    ],
  },
  diet_type: {
    label: "What type of diet do you follow?",
    options: [
      ["vegetarian", "Vegetarian"],
      ["non-vegetarian", "Non-vegetarian"],
      ["eggetarian", "Eggetarian"],
      ["vegan", "Vegan"],
    ],
  },
  activity_level: {
    label: "How often do you work out or exercise?",
    options: [
      ["low", "Rarely or just walks"],
      ["moderate", "1-3 times a week"],
      ["high", "4+ times a week"],
    ],
  },
  meals_per_day: {
    label: "How many meals do you usually eat per day?",
    options: [
      ["1-2", "1-2"],
      ["3", "3"],
      ["4+", "4 or more"],
    ],
  },
  fruit_veg_frequency: {
    label: "How often do you consume fruits and vegetables?",
    options: [
      ["daily", "Daily"],
      ["4-6_week", "4-6 times a week"],
      ["1-3_week", "1-3 times a week"],
      ["rarely", "Rarely"],
    ],
  },
  diet_trend: {
    label: "Which diet trend have you tried or been most tempted by?",
    options: [
      ["none", "None"],
      ["keto", "Keto"],
      ["intermittent_fasting", "Intermittent fasting"],
      ["detox_cleanse", "Detox / cleanse"],
      ["gm_diet", "GM diet"],
    ],
  },
  water_intake: {
    label: "How much water do you drink per day?",
    options: [
      ["1-2", "1-2 litres"],
      ["2-3", "2-3 litres"],
      ["gt_3", "More than 3 litres"],
      ["lt_1", "Less than 1 litre"],
    ],
  },
  carb_source: {
    label: "Which carbohydrate-rich foods do you consume most often?",
    options: [
      ["rice", "Rice"],
      ["wheat", "Wheat / roti / bread"],
      ["potatoes", "Potatoes"],
      ["fruits", "Fruits"],
      ["sweets", "Sugar / sweets"],
      ["processed", "Processed foods (biscuits, cakes, etc.)"],
      ["other", "Other / mixed"],
    ],
  },
  protein_source: {
    label: "Which protein-rich foods do you consume most frequently?",
    options: [
      ["pulses", "Pulses / legumes"],
      ["eggs", "Eggs"],
      ["dairy", "Milk / curd / cheese"],
      ["meat", "Meat / fish / chicken"],
      ["soy", "Soy products"],
      ["nuts", "Nuts and seeds"],
      ["other", "Other / mixed"],
    ],
  },
  fat_source: {
    label: "What are your main sources of dietary fats?",
    options: [
      ["oils", "Cooking oils"],
      ["ghee_butter", "Ghee / butter"],
      ["nuts", "Nuts and seeds"],
      ["fried_foods", "Fried foods"],
      ["dairy", "Dairy products"],
      ["other", "Other / mixed"],
    ],
  },
  post_carb_feeling: {
    label: "After eating carbohydrate-rich meals, how do you usually feel?",
    options: [
      ["energetic", "Energetic"],
      ["normal", "Normal"],
      ["sleepy_heavy", "Sleepy / heavy"],
    ],
  },
  breakfast_type: {
    label: "What do you usually have for breakfast or brunch?",
    options: [
      ["heavy", "Heavy breakfast like paratha, chole bhature, or similar"],
      ["quick", "Quick breakfast like poha, upma, chilla, toast, or muesli"],
      ["south_indian", "South Indian breakfast like idli, dosa, or vada"],
      ["tea_biscuits", "Mostly chai with biscuits or toast"],
      ["skip", "I usually skip it"],
    ],
  },
  dinner_type: {
    label: "What do you usually have for dinner?",
    options: [
      ["light", "Light meal like khichdi, curd rice, or simple dal-rice"],
      ["balanced", "Balanced home meal with roti or rice, sabzi, and dal"],
      ["one_pot", "One-pot meal like pulao, biryani, noodles, or pasta"],
      ["takeout", "Takeout or heavier outside food"],
    ],
  },
  goal_victory: {
    label: "If a diet plan could promise you one non-scale victory, what would you want most?",
    options: [
      ["more_energy", "More energy throughout the day"],
      ["better_sleep", "Better sleep"],
      ["clearer_skin", "Clearer skin"],
      ["feeling_stronger", "Feeling stronger"],
      ["no_afternoon_slump", "No more afternoon slump"],
    ],
  },
};

function QuestionCard({ name, value, onChange }) {
  const field = FIELD_META[name];

  return (
    <div className="form-field form-field-block">
      <span>{field.label}</span>
      <div className="choice-stack">
        {field.options.map(([optionValue, label]) => (
          <label key={optionValue} className={value === optionValue ? "choice-card active" : "choice-card"}>
            <input
              type="radio"
              name={name}
              value={optionValue}
              checked={value === optionValue}
              onChange={onChange}
            />
            <span>{label}</span>
          </label>
        ))}
      </div>
    </div>
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
  const activeStep = SURVEY_STEPS[step];

  return (
    <section className="assessment-section" id="assessment">
      <div className="assessment-copy">
        <SectionHeading
          eyebrow="Survey"
          title="Answer the survey and generate a starting plate from your real eating pattern."
          body="Once the survey is done, the app creates a plate from your answers. Then you can fix that plate and see exactly what changed."
        />
        <div className="survey-progress-card">
          <span>Step {step + 1} of {totalSteps}</span>
          <strong>{activeStep.title}</strong>
          <p>{activeStep.body}</p>
          <div className="survey-progress-bar">
            <div style={{ width: `${((step + 1) / totalSteps) * 100}%` }} />
          </div>
        </div>
        <ul className="assessment-notes">
          <li>Every question is multiple choice so the scoring stays consistent.</li>
          <li>The starting plate is generated directly from your meal, hydration, and food-group answers.</li>
          <li>The next screen lets you move into the plate-fix step with a full explanation.</li>
        </ul>
        <div className="survey-page-links">
          <button type="button" className="button button-secondary" onClick={() => onNavigate("quiz")}>
            Back to questions
          </button>
          <button type="button" className="button button-secondary" onClick={() => onNavigate("research")}>
            View research
          </button>
        </div>
      </div>

      <form className="assessment-form" onSubmit={onSubmit}>
        <div className="survey-step-header">
          <span className="eyebrow">Current step</span>
          <h3>{activeStep.title}</h3>
          <p>{activeStep.body}</p>
        </div>

        <div className="form-grid survey-grid">
          {activeStep.fields.map((fieldName) => (
            <QuestionCard
              key={fieldName}
              name={fieldName}
              value={form[fieldName]}
              onChange={onChange}
            />
          ))}
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
              {loading ? "Building your plate..." : "Generate my plate"}
            </button>
          )}
        </div>
      </form>
    </section>
  );
}
