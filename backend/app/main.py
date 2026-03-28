from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .content import CONTENT_SECTIONS
from .models import (
    AssessmentPayload,
    AssessmentResponse,
    ContentResponse,
    PlatePlanRequest,
    PlatePlanResponse,
    RecommendationResponse,
)
from .services.recommendations import (
    build_recommendations,
    compute_score,
    normalize_payload,
    optimize_plate,
)

app = FastAPI(
    title="Nutrition ML API",
    version="0.1.0",
    description="API for a research-led nutrition assessment and recommendation experience.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = Path(__file__).resolve().parent / "static"


@app.get("/health")
@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/content/sections", response_model=ContentResponse)
@app.get("/api/content/sections", response_model=ContentResponse)
def content_sections() -> ContentResponse:
    return ContentResponse(sections=CONTENT_SECTIONS)


@app.post("/assessment", response_model=AssessmentResponse)
@app.post("/api/assessment", response_model=AssessmentResponse)
def assessment(payload: AssessmentPayload) -> AssessmentResponse:
    normalized = normalize_payload(payload)
    return AssessmentResponse(
        status="received",
        normalized=normalized,
        score=compute_score(normalized),
    )


@app.post("/recommendations", response_model=RecommendationResponse)
@app.post("/api/recommendations", response_model=RecommendationResponse)
def recommendations(payload: AssessmentPayload) -> RecommendationResponse:
    return build_recommendations(payload)


@app.post("/plate/optimize", response_model=PlatePlanResponse)
@app.post("/api/plate/optimize", response_model=PlatePlanResponse)
def plate_optimize(payload: PlatePlanRequest) -> PlatePlanResponse:
    return optimize_plate(payload)


if STATIC_DIR.exists():
    app.mount("/assets", StaticFiles(directory=STATIC_DIR / "assets"), name="assets")

    @app.get("/")
    def serve_index() -> FileResponse:
        return FileResponse(STATIC_DIR / "index.html")
