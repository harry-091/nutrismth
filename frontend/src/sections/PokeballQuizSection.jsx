import SectionHeading from "../components/SectionHeading";

const QUIZ_QUESTIONS = [
  {
    prompt: "On average, how many meals do you eat per day?",
    options: ["1", "2", "3", "3+"],
    facts: {
      "1": "Eating only one meal a day often makes it harder to meet protein, fiber, and micronutrient needs consistently.",
      "2": "Two meals can work, but meal quality matters more because there are fewer chances to spread nutrients through the day.",
      "3": "Three meals usually make it easier to balance energy, hydration, and protein intake across the day.",
      "3+": "More than three eating occasions can work well if snacks are planned and not mostly packaged foods.",
    },
  },
  {
    prompt: "Let's start with breakfast or nashta. What does your morning meal usually look like?",
    options: [
      "Heavy — aloo paratha with butter, or chole bhature.",
      "Quick — poha, upma, chillas, or muesli.",
      "South Indian — idli, dosa, or vada with sambar.",
      "Just chai with biscuits or toast, or I skip it.",
    ],
    facts: {
      "Heavy — aloo paratha with butter, or chole bhature.": "Heavy breakfasts can keep you full longer, but they often work better when paired with hydration and a lighter rest of the day.",
      "Quick — poha, upma, chillas, or muesli.": "Quick breakfasts are often easier to sustain daily, especially if they include protein or fiber.",
      "South Indian — idli, dosa, or vada with sambar.": "Breakfasts with sambar or chutney can improve variety compared with tea-and-biscuit routines.",
      "Just chai with biscuits or toast, or I skip it.": "Skipping breakfast or relying only on chai and biscuits can leave the day low in protein and fiber.",
    },
  },
  {
    prompt: "Lunchtime. What's usually in your lunchbox or on your plate if you're home?",
    options: [
      "Classic — roti, sabzi, dal, and curd.",
      "Rice with sambar or rasam and curry.",
      "Leftovers from last night.",
      "Canteen or takeout — biryani, roll, or thali.",
    ],
    facts: {
      "Classic — roti, sabzi, dal, and curd.": "This kind of lunch already matches the balanced-plate idea better than most convenience meals.",
      "Rice with sambar or rasam and curry.": "A rice-based lunch works well when protein and vegetables are clearly present alongside it.",
      "Leftovers from last night.": "Leftovers can still be balanced if the original meal had vegetables, protein, and a steady carb source.",
      "Canteen or takeout — biryani, roll, or thali.": "Takeout lunches are not always bad, but they tend to vary more in oil, portion size, and vegetable quality.",
    },
  },
  {
    prompt: "What's a typical dinner meal for you?",
    options: [
      "Light — khichdi with curd, or simple dal-rice.",
      "Same as lunch — roti or rice with sabzi and dal.",
      "One-pot — pulao, biryani, or pasta.",
      "Takeout — parathas, Mughlai, or Chinese.",
    ],
    facts: {
      "Light — khichdi with curd, or simple dal-rice.": "Lighter dinners are often easier to digest, especially if the rest of the day was heavy.",
      "Same as lunch — roti or rice with sabzi and dal.": "Repeating a balanced lunch pattern at dinner can still support good routine consistency.",
      "One-pot — pulao, biryani, or pasta.": "One-pot meals work better when vegetables and a clear protein source are included.",
      "Takeout — parathas, Mughlai, or Chinese.": "Frequent takeout dinners often push up refined carbs, sodium, and oil intake.",
    },
  },
  {
    prompt: "What does your daily caffeine and hydration look like?",
    options: [
      "2–3 cups of chai or filter coffee, plus water.",
      "Coffee all day. Water could be better.",
      "Cutting down on chai — mostly water or nimbu pani.",
      "A lot of sodas, packaged juices, or sweet lassi.",
    ],
    facts: {
      "2–3 cups of chai or filter coffee, plus water.": "Caffeine habits matter less when water intake is still regular through the day.",
      "Coffee all day. Water could be better.": "Higher caffeine with lower water intake often shows up as a hydration consistency issue.",
      "Cutting down on chai — mostly water or nimbu pani.": "Replacing some caffeine with water-based drinks usually improves hydration patterns quickly.",
      "A lot of sodas, packaged juices, or sweet lassi.": "Sweetened drinks can crowd out water while also increasing sugar intake.",
    },
  },
  {
    prompt: "What's your main source of carbohydrate on a typical day?",
    options: [
      "Rice — every day.",
      "Roti or paratha — fresh.",
      "Oats, quinoa, or millets.",
      "Whatever comes with the meal.",
    ],
    facts: {
      "Rice — every day.": "Daily rice is not automatically unhealthy, but plate balance matters more when rice is the main carb each day.",
      "Roti or paratha — fresh.": "Fresh rotis can fit well into a balanced meal if vegetables and protein are also present.",
      "Oats, quinoa, or millets.": "These carbohydrate choices often add more fiber and variety to the diet.",
      "Whatever comes with the meal.": "When the carb source changes a lot, overall plate quality becomes more important than any one ingredient.",
    },
  },
  {
    prompt: "What's your main source of protein on a typical day?",
    options: [
      "Dal — almost daily.",
      "Chicken or fish — a few times a week.",
      "Paneer, soya, or legumes.",
      "Eggs — regularly.",
      "Not sure — whatever's in the meal.",
    ],
    facts: {
      "Dal — almost daily.": "Dal is one of the easiest regular protein anchors in many Indian meal patterns.",
      "Chicken or fish — a few times a week.": "Non-vegetarian protein sources can help, especially when they are not heavily fried.",
      "Paneer, soya, or legumes.": "Paneer, soya, and legumes can build strong vegetarian protein patterns.",
      "Eggs — regularly.": "Eggs are a simple protein source and often make breakfast or dinner easier to balance.",
      "Not sure — whatever's in the meal.": "If protein is unclear, it often means the meal is more carb-heavy than it needs to be.",
    },
  },
  {
    prompt: "What's your relationship with sweets?",
    options: [
      "Love them — jalebi, gulab jamun, mithai after meals.",
      "Sweet tooth, but mostly save it for festivals.",
      "A piece of chocolate or ice cream does it.",
      "Not into mithai — I prefer salty snacks.",
    ],
    facts: {
      "Love them — jalebi, gulab jamun, mithai after meals.": "Frequent sweets after meals can quietly push total sugar intake much higher than expected.",
      "Sweet tooth, but mostly save it for festivals.": "Occasional sweets are usually easier to manage than daily dessert routines.",
      "A piece of chocolate or ice cream does it.": "Smaller portions often make sweet habits easier to control without feeling restrictive.",
      "Not into mithai — I prefer salty snacks.": "Salty snack habits can still affect diet quality even if sugar is low.",
    },
  },
  {
    prompt: "How often do you work out or exercise?",
    options: [
      "Rarely — maybe a walk.",
      "1–2 times a week.",
      "3–4 times a week — consistent.",
      "Almost every day — non-negotiable.",
    ],
    facts: {
      "Rarely — maybe a walk.": "Lower activity usually increases the importance of meal quality and hydration consistency.",
      "1–2 times a week.": "Some activity is already helpful, even before moving to a more regular routine.",
      "3–4 times a week — consistent.": "Consistent activity often improves how well structured meal plans work.",
      "Almost every day — non-negotiable.": "Higher activity usually raises the importance of steady hydration and protein intake.",
    },
  },
  {
    prompt: "What's your typical sleep schedule like?",
    options: [
      "Disciplined — asleep by 10:30–11 PM, up by 6:30–7 AM.",
      "Midnight to 8 AM — fairly consistent.",
      "Varies — some days early, some nights up till 2–3 AM.",
      "Night owl — after 2 AM, struggle to wake up early.",
    ],
    facts: {
      "Disciplined — asleep by 10:30–11 PM, up by 6:30–7 AM.": "A stable sleep schedule usually supports better meal timing and appetite regulation.",
      "Midnight to 8 AM — fairly consistent.": "Consistency matters more than perfection when it comes to sleep and daily eating rhythm.",
      "Varies — some days early, some nights up till 2–3 AM.": "Irregular sleep can easily spill over into skipped meals and lower hydration.",
      "Night owl — after 2 AM, struggle to wake up early.": "Very late sleep schedules often make breakfast and hydration harder to manage consistently.",
    },
  },
];

export default function PokeballQuizSection({
  currentQuestion,
  selectedAnswer,
  onAnswer,
  onNext,
  answerCount,
  onNavigate,
}) {
  const question = QUIZ_QUESTIONS[currentQuestion];

  return (
    <section className="quiz-section">
      <div className="quiz-copy">
        <SectionHeading
          eyebrow="Questionnaire"
          title="Answer a few quick questions about your day-to-day routine."
          body="This section helps set context before the full survey and recommendation flow."
        />
        <div className="quiz-score">
          <span>Question {currentQuestion + 1} / {QUIZ_QUESTIONS.length}</span>
          <strong>{answerCount} answered</strong>
        </div>
        <div className="quiz-mini-nav">
          <button type="button" className="button button-secondary" onClick={() => onNavigate("home")}>
            Back home
          </button>
          <button type="button" className="button button-secondary" onClick={() => onNavigate("survey")}>
            Skip to survey
          </button>
        </div>
      </div>

      <div className="quiz-card">
        <div className="quiz-arena-glow" />
        <p className="quiz-prompt">{question.prompt}</p>

        <div className="quiz-option-list">
          {question.options.map((option) => (
            <button
              key={option}
              type="button"
              className={selectedAnswer === option ? "quiz-option-card active" : "quiz-option-card"}
              onClick={() => onAnswer(option)}
            >
              {option}
            </button>
          ))}
        </div>

        <div className="quiz-feedback">
          <p>
            {selectedAnswer
              ? question.facts[selectedAnswer]
              : "Choose one option to continue."}
          </p>
          <button
            type="button"
            className="button button-primary"
            onClick={onNext}
            disabled={!selectedAnswer}
          >
            {currentQuestion === QUIZ_QUESTIONS.length - 1 ? "Open the survey page" : "Next question"}
          </button>
        </div>
      </div>
    </section>
  );
}
