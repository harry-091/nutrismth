import SectionHeading from "../components/SectionHeading";

const QUIZ_QUESTIONS = [
  {
    prompt: "You need a quick morning drink choice before class. Which Pokeball do you open?",
    correct: "A bottle of water with breakfast",
    wrong: "A fizzy sugary drink on an empty stomach",
  },
  {
    prompt: "Lunch is rushed. Which option helps build a better plate?",
    correct: "Roti, dal, sabzi, and some curd",
    wrong: "Only instant noodles and chips",
  },
  {
    prompt: "It is snack time during study hours. What is the smarter pick?",
    correct: "Fruit with peanuts or seeds",
    wrong: "A second packet of fried snacks",
  },
  {
    prompt: "You want a better rice swap for a few meals this week. Which works?",
    correct: "Try brown rice or millet once or twice",
    wrong: "Skip lunch entirely",
  },
  {
    prompt: "You have not had many vegetables today. What helps most at dinner?",
    correct: "Add a half-plate of vegetables or salad",
    wrong: "Double the dessert instead",
  },
  {
    prompt: "You feel tired in the afternoon. Which habit is more helpful first?",
    correct: "Check water intake and eat a balanced snack",
    wrong: "Drink more sugary soda immediately",
  },
  {
    prompt: "Which daily habit supports better nutrition over time?",
    correct: "Consistent meals and hydration",
    wrong: "Random meals and frequent skipped breakfasts",
  },
];

function PokeballOption({ label, variant, onClick, state, disabled }) {
  return (
    <button
      type="button"
      className={`pokeball-option ${variant} ${state}`}
      onClick={onClick}
      disabled={disabled}
    >
      <span className="pokeball-top" />
      <span className="pokeball-center" />
      <span className="pokeball-label">{label}</span>
    </button>
  );
}

export default function PokeballQuizSection({
  currentQuestion,
  selectedAnswer,
  onAnswer,
  onNext,
  score,
  onNavigate,
}) {
  const question = QUIZ_QUESTIONS[currentQuestion];
  const answered = Boolean(selectedAnswer);

  function getState(option) {
    if (!selectedAnswer) {
      return "";
    }
    if (option === question.correct) {
      return "correct";
    }
    if (option === selectedAnswer) {
      return "wrong";
    }
    return "muted";
  }

  return (
    <section className="quiz-section">
      <div className="quiz-copy">
        <SectionHeading
          eyebrow="Quiz"
          title="Choose the Pokeball with the healthier habit."
          body="Pick the better option in each round, then continue to the full survey."
        />
        <div className="quiz-score">
          <span>Question {currentQuestion + 1} / 7</span>
          <strong>{score} healthy picks</strong>
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

        <div className="pokeball-grid">
          <PokeballOption
            label={question.correct}
            variant="pokeball-red"
            state={getState(question.correct)}
            disabled={answered}
            onClick={() => onAnswer(question.correct)}
          />
          <PokeballOption
            label={question.wrong}
            variant="pokeball-blue"
            state={getState(question.wrong)}
            disabled={answered}
            onClick={() => onAnswer(question.wrong)}
          />
        </div>

        {selectedAnswer ? (
          <div className="quiz-feedback">
            <p>
              {selectedAnswer === question.correct
                ? "Correct."
                : `The better pick here is: ${question.correct}.`}
            </p>
            <button type="button" className="button button-primary" onClick={onNext}>
              {currentQuestion === QUIZ_QUESTIONS.length - 1
                ? "Open the survey page"
                : "Next question"}
            </button>
          </div>
        ) : (
          <p className="quiz-hint">Tap one Pokeball to lock in your answer.</p>
        )}
      </div>
    </section>
  );
}
