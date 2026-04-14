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
        "age_group": "19-25",
        "gender": "female",
        "diet_type": "vegetarian",
        "meals_per_day": "3",
        "fruit_veg_frequency": "daily",
        "diet_trend": "none",
        "water_intake": "lt_1",
        "carb_source": "processed",
        "protein_source": "pulses",
        "fat_source": "fried_foods",
        "post_carb_feeling": "sleepy_heavy",
        "breakfast_type": "tea_biscuits",
        "dinner_type": "takeout",
        "goal_victory": "no_afternoon_slump",
        "activity_level": "moderate",
    }

    response = client.post("/recommendations", json=payload)
    body = response.json()

    assert response.status_code == 200
    assert body["user_summary"]["hydration_band"] == "Low hydration"
    assert body["hydration_recommendation"]["actions"]
    assert len(body["suggested_plate"]) == 4
    assert any(item["category"] == "protein" for item in body["suggested_plate"])


def test_assessment_validation_rejects_invalid_choices():
    payload = {
        "age_group": "19-25",
        "gender": "male",
        "diet_type": "vegetarian",
        "meals_per_day": "5",
        "fruit_veg_frequency": "daily",
        "diet_trend": "none",
        "water_intake": "2-3",
        "carb_source": "rice",
        "protein_source": "pulses",
        "fat_source": "oils",
        "post_carb_feeling": "normal",
        "breakfast_type": "quick",
        "dinner_type": "balanced",
        "goal_victory": "more_energy",
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
            "age_group": "19-25",
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
