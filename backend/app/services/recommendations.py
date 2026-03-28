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
        "fried chicken": {"updated": "grilled chicken", "kind": "heavy"},
        "grilled chicken": {"updated": "grilled chicken", "kind": "strong"},
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
    """Return normalized input while preserving the public schema."""
    return payload.model_copy(
        update={"water_intake_liters": round(payload.water_intake_liters, 1)}
    )


def compute_score(payload: AssessmentPayload) -> int:
    score = 50

    if payload.water_intake_liters >= 2.5:
        score += 15
    elif payload.water_intake_liters >= 1.6:
        score += 8
    else:
        score -= 12

    meal_adjustments = {"balanced": 12, "mixed": 4, "irregular": -10}
    produce_adjustments = {"daily": 12, "sometimes": 4, "rarely": -10}
    snack_adjustments = {"whole_food": 8, "mixed": 2, "packaged": -8}
    activity_adjustments = {"high": 8, "moderate": 4, "low": -4}

    score += meal_adjustments[payload.meal_pattern]
    score += produce_adjustments[payload.produce_frequency]
    score += snack_adjustments[payload.snack_preference]
    score += activity_adjustments[payload.activity_level]
    score -= min(payload.sugary_drinks_per_week * 2, 18)

    return max(0, min(100, score))


def build_recommendations(payload: AssessmentPayload) -> RecommendationResponse:
    normalized = normalize_payload(payload)
    score = compute_score(normalized)

    hydration_band = (
        "Needs immediate support"
        if normalized.water_intake_liters < 1.5
        else "Building consistency"
        if normalized.water_intake_liters < 2.3
        else "Strong routine"
    )
    meal_band = {
        "irregular": "Irregular eating rhythm",
        "mixed": "Partly structured meals",
        "balanced": "Balanced plate habits",
    }[normalized.meal_pattern]
    variety_band = {
        "rarely": "Low produce diversity",
        "sometimes": "Moderate variety",
        "daily": "High nutrient variety",
    }[normalized.produce_frequency]

    risk_indicators = [
        RiskIndicator(
            title="Hydration stability",
            level="high" if normalized.water_intake_liters < 1.5 else "medium" if normalized.water_intake_liters < 2.3 else "low",
            description=(
                "Daily water intake is likely limiting energy, appetite regulation, and routine consistency."
                if normalized.water_intake_liters < 1.5
                else "Hydration habits are improving but still benefit from timed prompts."
                if normalized.water_intake_liters < 2.3
                else "Water intake is supporting a stable baseline for daily nutrition choices."
            ),
        ),
        RiskIndicator(
            title="Meal quality",
            level="high" if normalized.meal_pattern == "irregular" else "medium" if normalized.meal_pattern == "mixed" else "low",
            description=(
                "Meal timing and composition suggest a high chance of convenience-led choices."
                if normalized.meal_pattern == "irregular"
                else "Some meals are balanced, but the overall pattern still needs more structure."
                if normalized.meal_pattern == "mixed"
                else "Meal pattern is already supportive of balanced plate guidance."
            ),
        ),
        RiskIndicator(
            title="Sugar displacement",
            level="high" if normalized.sugary_drinks_per_week >= 7 else "medium" if normalized.sugary_drinks_per_week >= 3 else "low",
            description=(
                "Frequent sugary drinks may be displacing water and increasing low-quality calorie intake."
                if normalized.sugary_drinks_per_week >= 7
                else "Reducing sweetened drinks a little more would noticeably improve the nutrition profile."
                if normalized.sugary_drinks_per_week >= 3
                else "Sugary drink intake is currently a minor concern compared with other habits."
            ),
        ),
    ]

    hydration_actions = [
        "Start the day with one full glass of water before tea, coffee, or breakfast.",
        "Use a bottle target: finish 1 bottle by midday and a second by evening.",
        "Pair each meal or snack with water instead of a sweetened drink.",
    ]
    if normalized.water_intake_liters >= 2.3:
        hydration_actions[1] = "Maintain the current routine and add hydration cues around activity or hot weather."

    swap_actions = [
        "Replace one refined-carb meal this week with millet, brown rice, or another whole-grain base.",
        "Move one packaged snack to fruit with nuts or seeds.",
        "Keep visible, ready-to-eat whole foods where convenient snacks usually win.",
    ]
    if normalized.snack_preference == "whole_food":
        swap_actions[1] = "Keep the whole-food snack habit and rotate ingredients to increase micronutrient variety."

    return RecommendationResponse(
        user_summary=UserSummary(
            hydration_band=hydration_band,
            meal_pattern_band=meal_band,
            nutrition_variety_band=variety_band,
        ),
        score=score,
        source="Rule-based recommendation engine seeded from the report themes",
        confidence_note="This version uses explainable nutrition rules and is designed to be replaced or extended by a future ML model.",
        risk_indicators=risk_indicators,
        hydration_recommendation=GuidanceCard(
            title="Hydration reset",
            summary="Small, timed hydration habits create the quickest visible improvement in daily nutrition stability.",
            actions=hydration_actions,
        ),
        plate_guidance=GuidanceCard(
            title="Build a more balanced plate",
            summary="Use an easy visual rule: half vegetables, a quarter protein, and a quarter smart carbohydrates.",
            actions=[
                "Anchor lunch or dinner with one half-plate of vegetables or salad.",
                "Add protein through pulses, paneer, eggs, curd, tofu, fish, or lean meat.",
                "Keep carb portions intentional by shifting from refined flour toward whole grains where possible.",
            ],
        ),
        smart_swaps=GuidanceCard(
            title="Make low-friction food swaps",
            summary="The goal is not restriction; it is reducing the number of default choices that work against nutrition quality.",
            actions=swap_actions,
        ),
        nutrient_education=GuidanceCard(
            title="Nutrients to pay attention to",
            summary="Balanced diets work best when they combine hydration, fiber, protein, and micronutrient-rich foods consistently.",
            actions=[
                "Vitamin- and mineral-rich foods improve recovery, concentration, and long-term health.",
                "Fiber from vegetables, fruit, legumes, and whole grains supports fullness and gut health.",
                "Protein distribution across the day helps build steadier energy than relying on one heavy meal.",
            ],
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
                reason = "Swap refined carbs for a steadier grain option."
            elif item.category == "protein" and kind == "heavy":
                reason = "Use a leaner protein choice to keep the plate more balanced."
            elif item.category == "vegetable" and kind in {"weak", "missing"}:
                reason = "Add vegetables so the plate has more fiber, volume, and micronutrients."
            elif item.category == "side" and kind == "weak":
                reason = "Change the side to something that supports hydration or nutrient quality."

        if payload.profile.goal == "higher_protein" and item.category == "protein":
            reason = "Keep a stronger protein portion for this goal."
            score += 5
        elif payload.profile.goal == "lighter_meal" and item.category == "side" and updated_name in {"fruit", "curd", "water"}:
            score += 4
        elif payload.profile.goal == "energy_support" and item.category == "base" and updated_name in {"brown rice", "millet", "multigrain roti"}:
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
        "side": "Water, curd, fruit, or nuts in a small portion",
    }

    tips = [
        f"Body weight: {int(payload.profile.body_weight_kg)} kg, so keep protein present in every main meal.",
        "If you are still hungry after this plate, add more vegetables or a protein side before adding more refined carbs.",
        goal_notes[payload.profile.goal],
    ]

    return PlatePlanResponse(
        score=score,
        summary="The plate has been adjusted to improve balance, fiber, and meal quality while matching the selected goal.",
        target_split=target_split,
        optimized_plate=optimized_items,
        adjustments=adjustments,
        tips=tips,
    )
