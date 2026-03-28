export default function HeroSection({ onNavigate }) {
  return (
    <section className="hero">
      <div className="hero-copy">
        <p className="eyebrow">NutriQuest</p>
        <h1>Better food habits start with small daily choices.</h1>
        <p className="hero-text">
          Explore hydration, balanced meals, smarter swaps, and a short survey
          that turns daily habits into practical nutrition guidance.
        </p>
        <div className="hero-actions">
          <button type="button" className="button button-primary" onClick={() => onNavigate("quiz")}>
            Start the game
          </button>
          <button type="button" className="button button-secondary" onClick={() => onNavigate("research")}>
            View research
          </button>
        </div>
      </div>

      <div className="hero-panel">
        <div className="hero-orbit hero-orbit-one" />
        <div className="hero-orbit hero-orbit-two" />
        <div className="hero-metric">
          <span>Focus</span>
          <strong>Hydration, balance, and better swaps</strong>
          <p>Simple guidance built around common eating patterns and daily routines.</p>
        </div>
        <div className="hero-grid">
          <article>
            <span>01</span>
            <h3>Hydration</h3>
            <p>Small reminders and simple goals instead of guilt.</p>
          </article>
          <article>
            <span>02</span>
            <h3>Plate balance</h3>
            <p>Make healthy meals look easy enough to try in real life.</p>
          </article>
          <article>
            <span>03</span>
            <h3>Food swaps</h3>
            <p>Swap habits gently instead of pretending everyone will eat perfectly.</p>
          </article>
          <article>
            <span>04</span>
            <h3>Mini game + survey</h3>
            <p>Start with the quiz, then continue into the survey and results.</p>
          </article>
        </div>
      </div>
    </section>
  );
}
