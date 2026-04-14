import { useEffect, useState, useTransition } from "react";
import HeroSection from "./sections/HeroSection";
import PokeballQuizSection from "./sections/PokeballQuizSection";
import ResearchSection from "./sections/ResearchSection";
import PillarsSection from "./sections/PillarsSection";
import AssessmentSection from "./sections/AssessmentSection";
import ResultsSection from "./sections/ResultsSection";
import PlatePlannerSection from "./sections/PlatePlannerSection";
import ModelInsightsSection from "./sections/ModelInsightsSection";
import { fetchRecommendations, fetchSections, optimizePlate, submitAssessment } from "./lib/api";
import { QUESTIONNAIRE_TOTAL } from "./lib/questionnaire";

const initialForm = {
  age_group: "18-25",
  gender: "female",
  water_intake_liters: 1.8,
  hydration_level: "medium",
  meal_pattern: "mixed",
  produce_frequency: "sometimes",
  snack_preference: "mixed",
  sugary_drinks_per_week: 3,
  activity_level: "moderate",
};

const initialPlateForm = {
  items: {
    base: "white rice",
    protein: "dal",
    vegetable: "sabzi",
    side: "fruit",
  },
  profile: {
    age_group: "18-25",
    gender: "female",
    body_weight_kg: 60,
    activity_level: "moderate",
    goal: "balanced",
  },
};

const PAGES = ["home", "quiz", "research", "model", "survey", "plate", "results"];

export default function App() {
  const [page, setPage] = useState(window.location.hash.replace("#", "") || "home");
  const [sections, setSections] = useState([]);
  const [form, setForm] = useState(initialForm);
  const [surveyStep, setSurveyStep] = useState(0);
  const [quizStep, setQuizStep] = useState(0);
  const [quizAnswers, setQuizAnswers] = useState([]);
  const [recommendations, setRecommendations] = useState(null);
  const [plateForm, setPlateForm] = useState(initialPlateForm);
  const [plateResult, setPlateResult] = useState(null);
  const [loadingSections, setLoadingSections] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isOptimizingPlate, setIsOptimizingPlate] = useState(false);
  const [formError, setFormError] = useState("");
  const [plateError, setPlateError] = useState("");
  const [pageError, setPageError] = useState("");
  const [isPending, startTransition] = useTransition();

  useEffect(() => {
    function syncPage() {
      const nextPage = window.location.hash.replace("#", "") || "home";
      setPage(PAGES.includes(nextPage) ? nextPage : "home");
    }

    window.addEventListener("hashchange", syncPage);
    syncPage();
    return () => window.removeEventListener("hashchange", syncPage);
  }, []);

  useEffect(() => {
    let cancelled = false;

    async function loadSections() {
      try {
        const data = await fetchSections();
        if (!cancelled) {
          setSections(data.sections);
        }
      } catch {
        if (!cancelled) {
          setPageError("Unable to load the research sections right now.");
        }
      } finally {
        if (!cancelled) {
          setLoadingSections(false);
        }
      }
    }

    loadSections();
    return () => {
      cancelled = true;
    };
  }, []);

  function handleChange(event) {
    const { name, value } = event.target;
    const numericFields = new Set(["water_intake_liters", "sugary_drinks_per_week"]);

    setForm((current) => ({
      ...current,
      [name]: numericFields.has(name) ? Number(value) : value,
    }));
  }

  function navigate(nextPage) {
    window.location.hash = nextPage;
  }

  const navItems = [
    ["home", "Home"],
    ["quiz", "Game"],
    ["research", "Research"],
    ["model", "Model"],
    ["survey", "Survey"],
    ["plate", "Plate"],
    ["results", "Results"],
  ];

  function handleQuizAnswer(answer) {
    setQuizAnswers((current) => {
      const next = [...current];
      next[quizStep] = answer;
      return next;
    });
  }

  function handleNextQuiz() {
    if (quizStep < QUESTIONNAIRE_TOTAL - 1) {
      setQuizStep((current) => current + 1);
      return;
    }
    navigate("survey");
  }

  function resetQuiz() {
    setQuizStep(0);
    setQuizAnswers([]);
  }

  function handleRetakeSurvey() {
    setForm(initialForm);
    setSurveyStep(0);
    setRecommendations(null);
    navigate("survey");
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setFormError("");
    setIsSubmitting(true);

    try {
      await submitAssessment(form);
      const data = await fetchRecommendations(form);
      startTransition(() => {
        setRecommendations(data);
      });
      navigate("results");
    } catch {
      setFormError("We could not generate recommendations. Please review the inputs and try again.");
    } finally {
      setIsSubmitting(false);
    }
  }

  function handlePlateItemChange(category, value) {
    setPlateForm((current) => ({
      ...current,
      items: {
        ...current.items,
        [category]: value,
      },
    }));
  }

  function handlePlateProfileChange(event) {
    const { name, value } = event.target;
    setPlateForm((current) => ({
      ...current,
      profile: {
        ...current.profile,
        [name]: name === "body_weight_kg" ? Number(value) : value,
      },
    }));
  }

  async function handlePlateSubmit(event) {
    event.preventDefault();
    setPlateError("");
    setIsOptimizingPlate(true);

    try {
      const payload = {
        items: Object.entries(plateForm.items).map(([category, name]) => ({ category, name })),
        profile: plateForm.profile,
      };
      const data = await optimizePlate(payload);
      setPlateResult(data);
    } catch {
      setPlateError("We could not adjust the plate right now.");
    } finally {
      setIsOptimizingPlate(false);
    }
  }

  return (
    <div className="page-shell">
      <header className="site-header">
        <div>
          <span className="brand-mark">NM</span>
          <div>
            <p>NutriQuest</p>
            <small>Nutrition habits and food choices</small>
          </div>
        </div>
        <nav>
          {navItems.map(([key, label]) => (
            <a
              key={key}
              href={`#${key}`}
              className={page === key ? "nav-link active" : "nav-link"}
            >
              {label}
            </a>
          ))}
        </nav>
      </header>

      <main>
        {page === "home" ? (
          <div className="page-view">
            <HeroSection onNavigate={navigate} />
            <PillarsSection />
          </div>
        ) : null}

        {page === "quiz" ? (
          <div className="page-view">
            <PokeballQuizSection
              currentQuestion={quizStep}
              selectedAnswer={quizAnswers[quizStep] ?? ""}
              onAnswer={handleQuizAnswer}
              onNext={handleNextQuiz}
              answerCount={quizAnswers.filter(Boolean).length}
              onNavigate={navigate}
              onReset={resetQuiz}
            />
          </div>
        ) : null}

        {page === "research" ? (
          <div className="page-view">
            {pageError ? <p className="page-error">{pageError}</p> : null}
            {!loadingSections && sections.length ? <ResearchSection sections={sections} /> : null}
          </div>
        ) : null}

        {page === "model" ? (
          <div className="page-view">
            <ModelInsightsSection />
          </div>
        ) : null}

        {page === "survey" ? (
          <div className="page-view">
            <AssessmentSection
              form={form}
              onChange={handleChange}
              onSubmit={handleSubmit}
              loading={isSubmitting || isPending}
              error={formError}
              step={surveyStep}
              totalSteps={4}
              onBack={() => setSurveyStep((current) => Math.max(0, current - 1))}
              onNextStep={() => setSurveyStep((current) => Math.min(3, current + 1))}
              onNavigate={navigate}
            />
          </div>
        ) : null}

        {page === "plate" ? (
          <div className="page-view">
            <PlatePlannerSection
              plateForm={plateForm}
              onPlateItemChange={handlePlateItemChange}
              onProfileChange={handlePlateProfileChange}
              onSubmit={handlePlateSubmit}
              loading={isOptimizingPlate}
              data={plateResult}
              error={plateError}
              onNavigate={navigate}
            />
          </div>
        ) : null}

        {page === "results" ? (
          <div className="page-view">
            <ResultsSection
              data={recommendations}
              onNavigate={navigate}
              onRetakeSurvey={handleRetakeSurvey}
            />
          </div>
        ) : null}
      </main>
    </div>
  );
}
