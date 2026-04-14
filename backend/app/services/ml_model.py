from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import joblib

from ..models import AssessmentPayload, ModelMetricsResponse, PlateItem


ARTIFACT_PATH = Path(__file__).resolve().parent.parent / "ml_artifacts" / "nutrition_model.joblib"

FEATURE_FIELDS = [
    "age_group",
    "gender",
    "diet_type",
    "meals_per_day",
    "fruit_veg_frequency",
    "diet_trend",
    "water_intake",
    "carb_source",
    "protein_source",
    "fat_source",
    "post_carb_feeling",
    "breakfast_type",
    "dinner_type",
    "goal_victory",
    "activity_level",
]


@dataclass
class MLPrediction:
    score: int
    hydration_band: str
    meal_rhythm_band: str
    nutrition_variety_band: str
    suggested_plate: list[PlateItem]


def _payload_to_features(payload: AssessmentPayload) -> dict[str, str]:
    return {field: getattr(payload, field) for field in FEATURE_FIELDS}


@lru_cache(maxsize=1)
def _load_bundle() -> dict[str, Any] | None:
    if not ARTIFACT_PATH.exists():
        return None
    return joblib.load(ARTIFACT_PATH)


def model_is_available() -> bool:
    return _load_bundle() is not None


def predict_assessment(payload: AssessmentPayload) -> MLPrediction | None:
    bundle = _load_bundle()
    if not bundle:
        return None

    vectorizer = bundle["vectorizer"]
    features = vectorizer.transform([_payload_to_features(payload)])

    score = round(float(bundle["score_model"].predict(features)[0]))
    hydration_band = str(bundle["band_models"]["hydration_band"].predict(features)[0])
    meal_rhythm_band = str(bundle["band_models"]["meal_rhythm_band"].predict(features)[0])
    nutrition_variety_band = str(bundle["band_models"]["nutrition_variety_band"].predict(features)[0])

    suggested_plate = [
        PlateItem(category="base", name=str(bundle["plate_models"]["base"].predict(features)[0])),
        PlateItem(category="protein", name=str(bundle["plate_models"]["protein"].predict(features)[0])),
        PlateItem(category="vegetable", name=str(bundle["plate_models"]["vegetable"].predict(features)[0])),
        PlateItem(category="side", name=str(bundle["plate_models"]["side"].predict(features)[0])),
    ]

    return MLPrediction(
        score=max(0, min(100, score)),
        hydration_band=hydration_band,
        meal_rhythm_band=meal_rhythm_band,
        nutrition_variety_band=nutrition_variety_band,
        suggested_plate=suggested_plate,
    )


def get_model_metrics() -> ModelMetricsResponse | None:
    bundle = _load_bundle()
    if not bundle:
        return None

    metadata = bundle["metadata"]
    return ModelMetricsResponse(
        model_name=metadata["model_name"],
        training_source=metadata["training_source"],
        sample_count=metadata["sample_count"],
        training_log=metadata["training_log"],
        score_mae=metadata["score_mae"],
        score_r2=metadata["score_r2"],
        hydration_accuracy=metadata["hydration_accuracy"],
        meal_rhythm_accuracy=metadata["meal_rhythm_accuracy"],
        variety_accuracy=metadata["variety_accuracy"],
        plate_accuracy=metadata["plate_accuracy"],
    )
