from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_content_sections_endpoint():
    response = client.get("/content/sections")
    body = response.json()

    assert response.status_code == 200
    assert len(body["sections"]) >= 3
    assert body["sections"][0]["slug"] == "problem"


def test_recommendations_happy_path():
    payload = {
        "age_group": "18-25",
        "gender": "female",
        "water_intake_liters": 1.2,
        "hydration_level": "low",
        "meal_pattern": "irregular",
        "produce_frequency": "sometimes",
        "snack_preference": "packaged",
        "sugary_drinks_per_week": 6,
        "activity_level": "moderate",
    }

    response = client.post("/recommendations", json=payload)
    body = response.json()

    assert response.status_code == 200
    assert body["user_summary"]["hydration_band"] == "Needs immediate support"
    assert body["hydration_recommendation"]["actions"]
    assert body["smart_swaps"]["actions"][0].startswith("Replace one refined-carb meal")


def test_assessment_validation_rejects_out_of_range_values():
    payload = {
        "age_group": "18-25",
        "gender": "male",
        "water_intake_liters": 10,
        "hydration_level": "medium",
        "meal_pattern": "balanced",
        "produce_frequency": "daily",
        "snack_preference": "whole_food",
        "sugary_drinks_per_week": 1,
        "activity_level": "high",
    }

    response = client.post("/assessment", json=payload)

    assert response.status_code == 422


def test_plate_optimizer_returns_adjusted_plate():
    payload = {
        "items": [
            {"category": "base", "name": "white rice"},
            {"category": "protein", "name": "fried chicken"},
            {"category": "vegetable", "name": "none"},
            {"category": "side", "name": "soft drink"},
        ],
        "profile": {
            "age_group": "18-25",
            "gender": "male",
            "body_weight_kg": 72,
            "activity_level": "moderate",
            "goal": "balanced",
        },
    }

    response = client.post("/plate/optimize", json=payload)
    body = response.json()

    assert response.status_code == 200
    assert body["score"] > 0
    assert any(item["name"] == "Brown Rice" for item in body["optimized_plate"])
    assert any(change["updated"] == "Water" for change in body["adjustments"])
