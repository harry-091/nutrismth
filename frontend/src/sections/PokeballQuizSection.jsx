import SectionHeading from "../components/SectionHeading";

const QUIZ_QUESTIONS = [
  {
    prompt: "On average, how many meals do you eat per day?",
    options: ["1", "2", "3", "3+"],
  },
  {
    prompt: "Let's start with breakfast or nashta. What does your morning meal usually look like?",
    options: [
      "Heavy — aloo paratha with butter, or chole bhature.",
      "Quick — poha, upma, chillas, or muesli.",
      "South Indian — idli, dosa, or vada with sambar.",
      "Just chai with biscuits or toast, or I skip it.",
    ],
  },
  {
    prompt: "Lunchtime. What's usually in your lunchbox or on your plate if you're home?",
    options: [
      "Classic — roti, sabzi, dal, and curd.",
      "Rice with sambar or rasam and curry.",
      "Leftovers from last night.",
      "Canteen or takeout — biryani, roll, or thali.",
    ],
  },
  {
    prompt: "What's a typical dinner meal for you?",
    options: [
      "Light — khichdi with curd, or simple dal-rice.",
      "Same as lunch — roti or rice with sabzi and dal.",
      "One-pot — pulao, biryani, or pasta.",
      "Takeout — parathas, Mughlai, or Chinese.",
    ],
  },
  {
    prompt: "What does your daily caffeine and hydration look like?",
    options: [
      "2–3 cups of chai or filter coffee, plus water.",
      "Coffee all day. Water could be better.",
      "Cutting down on chai — mostly water or nimbu pani.",
      "A lot of sodas, packaged juices, or sweet lassi.",
    ],
  },
  {
    prompt: "What's your main source of carbohydrate on a typical day?",
    options: [
      "Rice — every day.",
      "Roti or paratha — fresh.",
      "Oats, quinoa, or millets.",
      "Whatever comes with the meal.",
    ],
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
  },
  {
    prompt: "What's your relationship with sweets?",
    options: [
      "Love them — jalebi, gulab jamun, mithai after meals.",
      "Sweet tooth, but mostly save it for festivals.",
      "A piece of chocolate or ice cream does it.",
      "Not into mithai — I prefer salty snacks.",
    ],
  },
  {
    prompt: "How often do you work out or exercise?",
    options: [
      "Rarely — maybe a walk.",
      "1–2 times a week.",
      "3–4 times a week — consistent.",
      "Almost every day — non-negotiable.",
    ],
  },
  {
    prompt: "What's your typical sleep schedule like?",
    options: [
      "Disciplined — asleep by 10:30–11 PM, up by 6:30–7 AM.",
      "Midnight to 8 AM — fairly consistent.",
      "Varies — some days early, some nights up till 2–3 AM.",
      "Night owl — after 2 AM, struggle to wake up early.",
    ],
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
          <p>{selectedAnswer ? "Answer saved." : "Choose one option to continue."}</p>
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
