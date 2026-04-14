import SectionHeading from "../components/SectionHeading";
import { QUESTIONNAIRE, QUESTIONNAIRE_TOTAL } from "../lib/questionnaire";

export default function PokeballQuizSection({
  currentQuestion,
  selectedAnswer,
  onAnswer,
  onNext,
  answerCount,
  onNavigate,
  onReset,
}) {
  const question = QUESTIONNAIRE[currentQuestion];

  return (
    <section className="quiz-section">
      <div className="quiz-copy">
        <SectionHeading
          eyebrow="Questionnaire"
          title="Answer a few quick questions about your day-to-day routine."
          body="This section helps set context before the full survey and recommendation flow."
        />
        <div className="quiz-score">
          <span>Question {currentQuestion + 1} / {QUESTIONNAIRE_TOTAL}</span>
          <strong>{answerCount} answered</strong>
        </div>
        <div className="quiz-mini-nav">
          <button type="button" className="button button-secondary" onClick={() => onNavigate("home")}>
            Back home
          </button>
          <button type="button" className="button button-secondary" onClick={() => onNavigate("survey")}>
            Skip to survey
          </button>
          <button type="button" className="button button-secondary" onClick={onReset}>
            Restart questions
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
          {selectedAnswer ? (
            <div className="quiz-fact-card">
              <p>{question.facts[selectedAnswer]}</p>
            </div>
          ) : (
            <p>Choose one option to continue.</p>
          )}
          <button
            type="button"
            className="button button-primary"
            onClick={onNext}
            disabled={!selectedAnswer}
          >
            {currentQuestion === QUESTIONNAIRE_TOTAL - 1 ? "Open the survey page" : "Next question"}
          </button>
        </div>
      </div>
    </section>
  );
}
