from __future__ import annotations

from ..models import (
    AssessmentPayload,
    GuidanceCard,
    PlateItem,
    PlatePlanRequest,
    PlatePlanResponse,
    PlateSuggestion,
    RecommendationResponse,
    RiskIndicator,
    UserSummary,
)
from .ml_model import model_is_available, predict_assessment


PLATE_LIBRARY = {
    "base": {
        "white rice": {"updated": "brown rice", "kind": "refined"},
        "brown rice": {"updated": "brown rice", "kind": "smart"},
        "millet": {"updated": "millet", "kind": "smart"},
        "roti": {"updated": "multigrain roti", "kind": "balanced"},
        "multigrain roti": {"updated": "multigrain roti", "kind": "smart"},
        "quinoa": {"updated": "quinoa", "kind": "smart"},
        "oats": {"updated": "oats", "kind": "smart"},
        "poha": {"updated": "poha", "kind": "balanced"},
        "idli": {"updated": "idli", "kind": "balanced"},
        "dosa": {"updated": "dosa", "kind": "balanced"},
        "upma": {"updated": "upma", "kind": "balanced"},
        "noodles": {"updated": "millet noodles", "kind": "refined"},
        "millet noodles": {"updated": "millet noodles", "kind": "smart"},
    },
    "protein": {
        "paneer": {"updated": "paneer", "kind": "strong"},
        "dal": {"updated": "dal", "kind": "strong"},
        "rajma": {"updated": "rajma", "kind": "strong"},
        "chole": {"updated": "chole", "kind": "strong"},
        "eggs": {"updated": "eggs", "kind": "strong"},
        "grilled chicken": {"updated": "grilled chicken", "kind": "strong"},
        "fried chicken": {"updated": "grilled chicken", "kind": "heavy"},
        "fish": {"updated": "fish", "kind": "strong"},
        "tofu": {"updated": "tofu", "kind": "strong"},
        "soy chunks": {"updated": "soy chunks", "kind": "strong"},
        "curd": {"updated": "curd", "kind": "light"},
    },
    "vegetable": {
        "salad": {"updated": "salad", "kind": "strong"},
        "sabzi": {"updated": "sabzi", "kind": "strong"},
        "mixed vegetables": {"updated": "mixed vegetables", "kind": "strong"},
        "spinach": {"updated": "spinach", "kind": "strong"},
        "broccoli": {"updated": "broccoli", "kind": "strong"},
        "cucumber": {"updated": "cucumber", "kind": "strong"},
        "carrot": {"updated": "carrot", "kind": "strong"},
        "sauteed vegetables": {"updated": "sauteed vegetables", "kind": "strong"},
        "potato fries": {"updated": "sauteed vegetables", "kind": "weak"},
        "none": {"updated": "salad", "kind": "missing"},
    },
    "side": {
        "fruit": {"updated": "fruit", "kind": "smart"},
        "curd": {"updated": "curd", "kind": "smart"},
        "buttermilk": {"updated": "buttermilk", "kind": "smart"},
        "water": {"updated": "water", "kind": "smart"},
        "chips": {"updated": "fruit", "kind": "weak"},
        "soft drink": {"updated": "water", "kind": "weak"},
        "nuts and seeds": {"updated": "nuts and seeds", "kind": "smart"},
        "sprouts": {"updated": "sprouts", "kind": "smart"},
        "pickle": {"updated": "curd", "kind": "weak"},
    },
}


def normalize_payload(payload: AssessmentPayload) -> AssessmentPayload:
    return payload


def compute_rule_score(payload: AssessmentPayload) -> int:
    score = 55

    score += {"lt_1": -14, "1-2": -6, "2-3": 6, "gt_3": 10}[payload.water_intake]
    score += {"1-2": -8, "3": 6, "4+": 2}[payload.meals_per_day]
    score += {"daily": 10, "4-6_week": 6, "1-3_week": -2, "rarely": -10}[payload.fruit_veg_frequency]
    score += {"rice": 1, "wheat": 2, "potatoes": -2, "fruits": 4, "sweets": -8, "processed": -10, "other": 0}[payload.carb_source]
    score += {"pulses": 8, "eggs": 7, "dairy": 4, "meat": 8, "soy": 8, "nuts": 4, "other": -2}[payload.protein_source]
    score += {"oils": 1, "ghee_butter": -1, "nuts": 4, "fried_foods": -7, "dairy": 0, "other": -1}[payload.fat_source]
    score += {"energetic": 4, "normal": 1, "sleepy_heavy": -6}[payload.post_carb_feeling]
    score += {"heavy": -3, "quick": 3, "south_indian": 2, "tea_biscuits": -7, "skip": -8}[payload.breakfast_type]
    score += {"light": 5, "balanced": 4, "one_pot": -2, "takeout": -8}[payload.dinner_type]
    score += {"low": -4, "moderate": 3, "high": 7}[payload.activity_level]
    score += {"none": 2, "intermittent_fasting": -1, "keto": -2, "detox_cleanse": -5, "gm_diet": -5}[payload.diet_trend]

    return max(0, min(100, score))


def derive_rule_suggested_plate(payload: AssessmentPayload) -> list[PlateItem]:
    base = {
        "rice": "white rice",
        "wheat": "roti",
        "potatoes": "roti",
        "fruits": "oats",
        "sweets": "white rice",
        "processed": "noodles",
        "other": "millet",
    }[payload.carb_source]

    protein = {
        "pulses": "dal",
        "eggs": "eggs",
        "dairy": "paneer",
        "meat": "grilled chicken",
        "soy": "tofu" if payload.diet_type == "vegan" else "soy chunks",
        "nuts": "curd",
        "other": "dal",
    }[payload.protein_source]

    vegetable = "salad" if payload.fruit_veg_frequency in {"daily", "4-6_week"} else "sabzi" if payload.fruit_veg_frequency == "1-3_week" else "none"

    side = (
        "water"
        if payload.water_intake in {"2-3", "gt_3"}
        else "buttermilk"
        if payload.goal_victory in {"better_sleep", "no_afternoon_slump"}
        else "fruit"
    )
    if payload.post_carb_feeling == "sleepy_heavy":
        side = "water"

    return [
        PlateItem(category="base", name=base.title()),
        PlateItem(category="protein", name=protein.title()),
        PlateItem(category="vegetable", name=vegetable.title()),
        PlateItem(category="side", name=side.title()),
    ]


def derive_rule_bands(payload: AssessmentPayload) -> tuple[str, str, str]:
    hydration_band = {
        "lt_1": "Low hydration",
        "1-2": "Needs improvement",
        "2-3": "Steady intake",
        "gt_3": "High intake",
    }[payload.water_intake]
    meal_band = {
        "1-2": "Low meal frequency",
        "3": "Steady meal rhythm",
        "4+": "Frequent eating pattern",
    }[payload.meals_per_day]
    variety_band = {
        "daily": "High variety",
        "4-6_week": "Good variety",
        "1-3_week": "Moderate variety",
        "rarely": "Low variety",
    }[payload.fruit_veg_frequency]
    return hydration_band, meal_band, variety_band


def compute_score(payload: AssessmentPayload) -> int:
    prediction = predict_assessment(payload)
    if prediction:
        return prediction.score
    return compute_rule_score(payload)


def derive_suggested_plate(payload: AssessmentPayload) -> list[PlateItem]:
    prediction = predict_assessment(payload)
    if prediction:
        return prediction.suggested_plate
    return derive_rule_suggested_plate(payload)


def build_recommendations(payload: AssessmentPayload) -> RecommendationResponse:
    normalized = normalize_payload(payload)
    prediction = predict_assessment(normalized)
    score = prediction.score if prediction else compute_rule_score(normalized)
    suggested_plate = prediction.suggested_plate if prediction else derive_rule_suggested_plate(normalized)
    hydration_band, meal_band, variety_band = (
        (
            prediction.hydration_band,
            prediction.meal_rhythm_band,
            prediction.nutrition_variety_band,
        )
        if prediction
        else derive_rule_bands(normalized)
    )

    risk_indicators = [
        RiskIndicator(
            title="Hydration quality",
            level="high" if normalized.water_intake == "lt_1" else "medium" if normalized.water_intake == "1-2" else "low",
            description="Water intake influences energy, appetite control, and how heavy meals feel through the day.",
        ),
        RiskIndicator(
            title="Meal quality",
            level="high" if normalized.breakfast_type in {"skip", "tea_biscuits"} or normalized.dinner_type == "takeout" else "medium" if normalized.dinner_type == "one_pot" else "low",
            description="Breakfast and dinner patterns often explain whether the daily routine is balanced or convenience-heavy.",
        ),
        RiskIndicator(
            title="Plate balance",
            level="high" if normalized.fruit_veg_frequency == "rarely" or normalized.post_carb_feeling == "sleepy_heavy" else "medium" if normalized.carb_source in {"rice", "wheat"} else "low",
            description="Carbohydrate-heavy meals without enough vegetables or protein often lead to afternoon heaviness and lower satiety.",
        ),
    ]

    hydration_actions = [
        "Aim for regular water intake through the day instead of catching up late in the evening.",
        "Pair chai or coffee with a glass of water so caffeine does not replace hydration.",
        "If you often feel sleepy after meals, improve water intake before changing meal quantity.",
    ]

    plate_actions = [
        f"Your starting plate uses {suggested_plate[0].name.lower()} as the main base and {suggested_plate[1].name.lower()} as the protein anchor.",
        "Try to keep vegetables visible on the plate instead of leaving them as a side thought.",
        "Use the fix-plate step to convert the starting meal into a more balanced version from the same food options.",
    ]

    swap_actions = [
        "If you rely on sweets or processed foods for carbohydrates, move toward roti, oats, millet, or brown rice more often.",
        "If protein is unclear in the meal, make it explicit by adding dal, eggs, paneer, soy, or lean meat.",
        "If your meals make you feel sleepy, reduce refined carbohydrates and improve plate balance first.",
    ]

    nutrient_actions = [
        "Fruits and vegetables improve fiber, micronutrients, and recovery across the week.",
        "Protein sources spread across meals help with satiety, strength, and steadier energy.",
        "Fat quality matters too: nuts and seeds support balance better than frequent fried foods.",
    ]

    return RecommendationResponse(
        user_summary=UserSummary(
            hydration_band=hydration_band,
            meal_rhythm_band=meal_band,
            nutrition_variety_band=variety_band,
        ),
        score=score,
        source=(
            "Trained decision-tree nutrition model served from local model artifacts"
            if model_is_available()
            else "Rule-based nutrition analysis built from the updated survey questionnaire"
        ),
        confidence_note=(
            "The live app is using a trained machine learning model built on a bootstrap nutrition dataset generated from the project logic. It is a real trained model, but not yet trained on real user outcome data."
            if model_is_available()
            else "This version uses a structured nutrition scoring model. The next step could be replacing these weighted rules with a trained ML model using real survey data."
        ),
        risk_indicators=risk_indicators,
        suggested_plate=suggested_plate,
        hydration_recommendation=GuidanceCard(
            title="Hydration focus",
            summary="Hydration is one of the fastest ways to improve how meals feel and how steady your energy stays.",
            actions=hydration_actions,
        ),
        plate_guidance=GuidanceCard(
            title="Generated plate",
            summary="A starting plate has been generated from your survey answers. You can now fix and rebalance it in the next step.",
            actions=plate_actions,
        ),
        smart_swaps=GuidanceCard(
            title="Carb and protein swaps",
            summary="Your answer pattern suggests a few direct swaps that can improve meal quality without changing the whole diet.",
            actions=swap_actions,
        ),
        nutrient_education=GuidanceCard(
            title="Nutrition notes",
            summary="The survey focuses on plate balance, hydration, meal rhythm, and how different food groups affect energy and recovery.",
            actions=nutrient_actions,
        ),
    )


def optimize_plate(payload: PlatePlanRequest) -> PlatePlanResponse:
    optimized_items: list[PlateItem] = []
    adjustments: list[PlateSuggestion] = []
    score = 58

    goal_notes = {
        "balanced": "Keep the plate even across vegetables, protein, and steady carbs.",
        "higher_protein": "Shift a little more space toward protein while keeping vegetables in the plate.",
        "lighter_meal": "Keep the meal lighter by reducing heavy sides and refined items.",
        "energy_support": "Use steady carbs, protein, and hydration-friendly sides for better energy through the day.",
    }

    seen_categories = {item.category for item in payload.items}
    if "vegetable" not in seen_categories:
        payload.items = payload.items + [PlateItem(category="vegetable", name="none")]

    for item in payload.items:
        library_item = PLATE_LIBRARY[item.category].get(item.name.lower())
        updated_name = item.name
        reason = "This item already fits the plate well."

        if library_item:
            updated_name = library_item["updated"]
            kind = library_item["kind"]

            if kind in {"refined", "weak", "heavy", "missing"}:
                score -= 2

            if item.category == "base" and kind == "refined":
                reason = "This base is a little heavier or more refined than needed, so it was swapped to a steadier carbohydrate source."
            elif item.category == "protein" and kind == "heavy":
                reason = "This protein choice was made lighter to improve balance while keeping protein quality strong."
            elif item.category == "vegetable" and kind in {"weak", "missing"}:
                reason = "The plate needed a clearer vegetable component for fiber, volume, and micronutrient support."
            elif item.category == "side" and kind == "weak":
                reason = "The side was changed to something that supports hydration or satiety more effectively."

        if payload.profile.goal == "higher_protein" and item.category == "protein":
            reason = "The plate keeps a stronger protein anchor because the selected goal is higher protein."
            score += 5
        elif payload.profile.goal == "lighter_meal" and item.category == "side" and updated_name in {"fruit", "curd", "water", "buttermilk"}:
            score += 4
        elif payload.profile.goal == "energy_support" and item.category == "base" and updated_name in {"brown rice", "millet", "multigrain roti", "quinoa", "oats"}:
            score += 4

        optimized_items.append(PlateItem(category=item.category, name=updated_name.title()))

        if updated_name.lower() != item.name.lower():
            adjustments.append(
                PlateSuggestion(
                    category=item.category,
                    original=item.name.title(),
                    updated=updated_name.title(),
                    reason=reason,
                )
            )

    if payload.profile.body_weight_kg >= 80 and payload.profile.goal != "higher_protein":
        score += 3
    if payload.profile.activity_level == "high":
        score += 4
    elif payload.profile.activity_level == "low":
        score -= 3

    score = max(0, min(100, score + 18))

    target_split = {
        "vegetables": "1/2 plate",
        "protein": "1/4 plate" if payload.profile.goal != "higher_protein" else "1/3 plate",
        "smart_carbs": "1/4 plate" if payload.profile.goal != "higher_protein" else "1/6 plate",
        "side": "Water, curd, fruit, buttermilk, or nuts in a small portion",
    }

    tips = [
        f"Body weight: {int(payload.profile.body_weight_kg)} kg, so protein should stay visible in the meal rather than being incidental.",
        "If the meal still feels too heavy after fixing the plate, reduce refined carbs before reducing vegetables or protein.",
        goal_notes[payload.profile.goal],
    ]

    return PlatePlanResponse(
        score=score,
        summary="The plate has been adjusted using the same allowed food options to improve balance, satiety, hydration support, and energy stability.",
        target_split=target_split,
        optimized_plate=optimized_items,
        adjustments=adjustments,
        tips=tips,
    )
