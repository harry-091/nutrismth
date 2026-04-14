from __future__ import annotations

import json
import sys
from pathlib import Path
from random import Random

import joblib
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

BACKEND_ROOT = Path(__file__).resolve().parent.parent
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.models import AssessmentPayload
from app.services.ml_model import ARTIFACT_PATH, FEATURE_FIELDS
from app.services.recommendations import (
    compute_rule_score,
    derive_rule_bands,
    derive_rule_suggested_plate,
)


OPTIONS = {
    "age_group": ["15-18", "19-25", "26-35", "35+"],
    "gender": ["female", "male"],
    "diet_type": ["vegetarian", "non-vegetarian", "eggetarian", "vegan"],
    "meals_per_day": ["1-2", "3", "4+"],
    "fruit_veg_frequency": ["daily", "4-6_week", "1-3_week", "rarely"],
    "diet_trend": ["none", "keto", "intermittent_fasting", "detox_cleanse", "gm_diet"],
    "water_intake": ["lt_1", "1-2", "2-3", "gt_3"],
    "carb_source": ["rice", "wheat", "potatoes", "fruits", "sweets", "processed", "other"],
    "protein_source": ["pulses", "eggs", "dairy", "meat", "soy", "nuts", "other"],
    "fat_source": ["oils", "ghee_butter", "nuts", "fried_foods", "dairy", "other"],
    "post_carb_feeling": ["energetic", "normal", "sleepy_heavy"],
    "breakfast_type": ["heavy", "quick", "south_indian", "tea_biscuits", "skip"],
    "dinner_type": ["light", "balanced", "one_pot", "takeout"],
    "goal_victory": ["more_energy", "better_sleep", "clearer_skin", "feeling_stronger", "no_afternoon_slump"],
    "activity_level": ["low", "moderate", "high"],
}

SAMPLE_COUNT = 12000
SEED = 42


def sample_payload(randomizer: Random) -> AssessmentPayload:
    data = {field: randomizer.choice(options) for field, options in OPTIONS.items()}
    return AssessmentPayload(**data)


def payload_to_features(payload: AssessmentPayload) -> dict[str, str]:
    return {field: getattr(payload, field) for field in FEATURE_FIELDS}


def build_dataset(sample_count: int = SAMPLE_COUNT, seed: int = SEED):
    randomizer = Random(seed)
    rows = []
    labels = {
        "score": [],
        "hydration_band": [],
        "meal_rhythm_band": [],
        "nutrition_variety_band": [],
        "base": [],
        "protein": [],
        "cooked_veg": [],
        "fresh_side": [],
        "drink": [],
        "add_on": [],
    }

    for _ in range(sample_count):
        payload = sample_payload(randomizer)
        rows.append(payload_to_features(payload))

        score = compute_rule_score(payload)
        hydration_band, meal_rhythm_band, variety_band = derive_rule_bands(payload)
        plate = derive_rule_suggested_plate(payload)

        labels["score"].append(score)
        labels["hydration_band"].append(hydration_band)
        labels["meal_rhythm_band"].append(meal_rhythm_band)
        labels["nutrition_variety_band"].append(variety_band)
        labels["base"].append(plate[0].name)
        labels["protein"].append(plate[1].name)
        labels["cooked_veg"].append(plate[2].name)
        labels["fresh_side"].append(plate[3].name)
        labels["drink"].append(plate[4].name)
        labels["add_on"].append(plate[5].name)

    return rows, labels


def train_and_save():
    training_log = [
        "Starting training run with bootstrap nutrition dataset generation.",
        f"Sampling {SAMPLE_COUNT} survey records across all questionnaire feature combinations using seed {SEED}.",
        "Encoding categorical survey answers with DictVectorizer.",
        "Splitting dataset into training and test partitions with an 80/20 split.",
        "Training LinearRegression for nutrition score prediction.",
        "Training DecisionTreeClassifier models for hydration, meal rhythm, and nutrition variety bands.",
        "Training DecisionTreeClassifier models for base, protein, cooked veg, fresh side, drink, and add-on plate generation.",
        "Evaluating regression with MAE and R2, and classification tasks with accuracy.",
        "Saving the fitted model bundle and metrics JSON into backend/app/ml_artifacts.",
    ]

    rows, labels = build_dataset()
    vectorizer = DictVectorizer(sparse=True)
    features = vectorizer.fit_transform(rows)

    indices = list(range(len(rows)))
    train_indices, test_indices = train_test_split(indices, test_size=0.2, random_state=SEED)

    x_train = features[train_indices]
    x_test = features[test_indices]

    score_model = LinearRegression()
    score_model.fit(x_train, [labels["score"][index] for index in train_indices])
    score_predictions = score_model.predict(x_test)

    band_models = {}
    band_metrics = {}
    for label_name in ["hydration_band", "meal_rhythm_band", "nutrition_variety_band"]:
        model = DecisionTreeClassifier(random_state=SEED)
        model.fit(x_train, [labels[label_name][index] for index in train_indices])
        predictions = model.predict(x_test)
        band_models[label_name] = model
        band_metrics[label_name] = accuracy_score(
            [labels[label_name][index] for index in test_indices],
            predictions,
        )

    plate_models = {}
    plate_accuracy = {}
    for category in ["base", "protein", "cooked_veg", "fresh_side", "drink", "add_on"]:
        model = DecisionTreeClassifier(random_state=SEED)
        model.fit(x_train, [labels[category][index] for index in train_indices])
        predictions = model.predict(x_test)
        plate_models[category] = model
        plate_accuracy[category] = accuracy_score(
            [labels[category][index] for index in test_indices],
            predictions,
        )

    metadata = {
        "model_name": "Linear-score plus decision-tree nutrition model",
        "training_source": "Synthetic bootstrap dataset generated from project nutrition rules",
        "sample_count": len(rows),
        "training_log": training_log,
        "score_mae": round(mean_absolute_error([labels["score"][index] for index in test_indices], score_predictions), 4),
        "score_r2": round(r2_score([labels["score"][index] for index in test_indices], score_predictions), 4),
        "hydration_accuracy": round(band_metrics["hydration_band"], 4),
        "meal_rhythm_accuracy": round(band_metrics["meal_rhythm_band"], 4),
        "variety_accuracy": round(band_metrics["nutrition_variety_band"], 4),
        "plate_accuracy": {key: round(value, 4) for key, value in plate_accuracy.items()},
    }

    ARTIFACT_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "vectorizer": vectorizer,
            "score_model": score_model,
            "band_models": band_models,
            "plate_models": plate_models,
            "metadata": metadata,
        },
        ARTIFACT_PATH,
    )

    metrics_path = ARTIFACT_PATH.with_suffix(".json")
    metrics_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    train_and_save()
