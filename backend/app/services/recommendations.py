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
        "brown rice": {"kind": "smart"},
        "multigrain roti": {"kind": "smart"},
        "millet khichdi": {"kind": "smart"},
        "quinoa pulao": {"kind": "smart"},
        "oats chilla": {"kind": "smart"},
        "idli": {"kind": "balanced"},
        "poha": {"kind": "balanced"},
        "sweet potato bowl": {"kind": "smart"},
        "white rice": {"kind": "refined"},
        "butter naan": {"kind": "heavy"},
        "instant noodles": {"kind": "refined"},
        "creamy pasta": {"kind": "heavy"},
    },
    "protein": {
        "dal tadka": {"kind": "strong"},
        "rajma masala": {"kind": "strong"},
        "chickpea curry": {"kind": "strong"},
        "paneer tikka": {"kind": "strong"},
        "egg bhurji": {"kind": "strong"},
        "grilled chicken": {"kind": "strong"},
        "fish curry": {"kind": "strong"},
        "tofu stir-fry": {"kind": "strong"},
        "soy chunk masala": {"kind": "strong"},
        "hung curd dip": {"kind": "light"},
        "fried chicken": {"kind": "heavy"},
        "creamy paneer": {"kind": "heavy"},
    },
    "cooked_veg": {
        "bhindi sabzi": {"kind": "strong"},
        "lauki sabzi": {"kind": "strong"},
        "spinach corn": {"kind": "strong"},
        "cabbage peas": {"kind": "strong"},
        "roasted broccoli": {"kind": "strong"},
        "mixed veg stir-fry": {"kind": "strong"},
        "pumpkin sabzi": {"kind": "strong"},
        "mushroom pepper saute": {"kind": "strong"},
        "potato fries": {"kind": "weak"},
        "crispy corn": {"kind": "weak"},
        "none": {"kind": "missing"},
    },
    "fresh_side": {
        "cucumber salad": {"kind": "smart"},
        "kachumber salad": {"kind": "smart"},
        "fruit bowl": {"kind": "smart"},
        "sprout chaat": {"kind": "smart"},
        "carrot sticks": {"kind": "smart"},
        "tomato onion salad": {"kind": "smart"},
        "mint yogurt salad": {"kind": "smart"},
        "none": {"kind": "missing"},
        "nachos": {"kind": "weak"},
        "cream biscuit": {"kind": "weak"},
    },
    "drink": {
        "water": {"kind": "smart"},
        "buttermilk": {"kind": "smart"},
        "lemon water": {"kind": "smart"},
        "coconut water": {"kind": "smart"},
        "unsweetened chai": {"kind": "balanced"},
        "plain lassi": {"kind": "balanced"},
        "sweet soda": {"kind": "weak"},
        "packaged juice": {"kind": "weak"},
        "milkshake": {"kind": "heavy"},
    },
    "add_on": {
        "curd bowl": {"kind": "smart"},
        "roasted makhana": {"kind": "smart"},
        "nuts and seeds": {"kind": "smart"},
        "peanut chutney": {"kind": "balanced"},
        "hummus": {"kind": "smart"},
        "pickle": {"kind": "weak"},
        "gulab jamun": {"kind": "weak"},
        "salted chips": {"kind": "weak"},
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
        "rice": "brown rice",
        "wheat": "multigrain roti",
        "potatoes": "sweet potato bowl",
        "fruits": "oats chilla",
        "sweets": "millet khichdi",
        "processed": "quinoa pulao",
        "other": "millet khichdi",
    }[payload.carb_source]

    protein = {
        "pulses": "dal tadka",
        "eggs": "egg bhurji",
        "dairy": "paneer tikka",
        "meat": "grilled chicken",
        "soy": "tofu stir-fry" if payload.diet_type == "vegan" else "soy chunk masala",
        "nuts": "hung curd dip",
        "other": "chickpea curry",
    }[payload.protein_source]

    cooked_veg = (
        "roasted broccoli"
        if payload.goal_victory in {"clearer_skin", "more_energy"}
        else "spinach corn"
        if payload.fruit_veg_frequency in {"daily", "4-6_week"}
        else "mixed veg stir-fry"
        if payload.fruit_veg_frequency == "1-3_week"
        else "lauki sabzi"
    )
    fresh_side = (
        "sprout chaat"
        if payload.goal_victory == "feeling_stronger"
        else "fruit bowl"
        if payload.post_carb_feeling == "sleepy_heavy"
        else "kachumber salad"
        if payload.fruit_veg_frequency in {"daily", "4-6_week"}
        else "cucumber salad"
    )
    drink = (
        "water"
        if payload.water_intake in {"2-3", "gt_3"}
        else "buttermilk"
        if payload.goal_victory in {"better_sleep", "no_afternoon_slump"}
        else "lemon water"
    )
    add_on = (
        "nuts and seeds"
        if payload.goal_victory in {"clearer_skin", "more_energy"}
        else "roasted makhana"
        if payload.goal_victory == "better_sleep"
        else "curd bowl"
    )

    return [
        PlateItem(category="base", name=base.title()),
        PlateItem(category="protein", name=protein.title()),
        PlateItem(category="cooked_veg", name=cooked_veg.title()),
        PlateItem(category="fresh_side", name=fresh_side.title()),
        PlateItem(category="drink", name=drink.title()),
        PlateItem(category="add_on", name=add_on.title()),
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
        "The fresh side, drink, and add-on were chosen to support hydration and balance around the main meal.",
        "You can edit any plate section and the live plate score will update immediately.",
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
            summary="A balanced plate has been generated from your survey answers and can be adjusted live without leaving the planner.",
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
    score = 62

    goal_notes = {
        "balanced": "Keep the plate even across vegetables, protein, and steady carbs.",
        "higher_protein": "Shift a little more space toward protein while keeping vegetables in the plate.",
        "lighter_meal": "Keep the meal lighter by reducing heavy sides and refined items.",
        "energy_support": "Use steady carbs, protein, and hydration-friendly sides for better energy through the day.",
    }

    for item in payload.items:
        library_item = PLATE_LIBRARY[item.category].get(item.name.lower())
        selected_name = item.name
        reason = "This choice supports the plate well."

        if library_item:
            kind = library_item["kind"]

            if kind == "smart":
                score += 4
                reason = "This is a strong pick for this section and helps overall plate quality."
            elif kind == "strong":
                score += 5
                reason = "This section adds strong nutritional value and improves the overall balance."
            elif kind in {"balanced", "light"}:
                score += 2
                reason = "This works well here and keeps the plate practical without overloading it."
            elif kind == "refined":
                score -= 6
                reason = "This option is more refined than ideal, so the plate score drops a bit."
            elif kind == "heavy":
                score -= 8
                reason = "This option makes the plate heavier and less steady for energy."
            elif kind == "weak":
                score -= 7
                reason = "This choice adds less nutrition support than the other available options."
            elif kind == "missing":
                score -= 10
                reason = "Leaving this section empty makes the plate less balanced."

            if item.category == "base" and kind in {"refined", "heavy"}:
                score -= 2
            if item.category == "protein" and kind in {"strong", "smart"}:
                score += 2
            if item.category in {"cooked_veg", "fresh_side"} and kind in {"strong", "smart"}:
                score += 2
            if item.category == "drink" and selected_name.lower() in {"water", "buttermilk", "lemon water", "coconut water"}:
                score += 3
            if item.category == "drink" and kind in {"weak", "heavy"}:
                score -= 4
            if item.category == "add_on" and kind == "smart":
                score += 2

        if payload.profile.goal == "higher_protein" and item.category == "protein" and library_item and library_item["kind"] in {"strong", "smart"}:
            score += 5
            reason = "This protein choice matches the higher-protein goal especially well."
        elif payload.profile.goal == "lighter_meal" and item.category in {"fresh_side", "drink", "add_on"} and library_item and library_item["kind"] in {"smart", "balanced", "light"}:
            score += 4
        elif payload.profile.goal == "energy_support" and item.category == "base" and selected_name.lower() in {"brown rice", "multigrain roti", "millet khichdi", "quinoa pulao", "oats chilla", "sweet potato bowl"}:
            score += 4

        optimized_items.append(PlateItem(category=item.category, name=selected_name.title()))
        adjustments.append(
            PlateSuggestion(
                category=item.category,
                original=item.name.title(),
                updated=item.name.title(),
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
        "base": "Choose one steady carbohydrate anchor",
        "protein": "Make this the strongest visible section after vegetables",
        "vegetables": "Use both cooked and fresh sections for variety and fiber",
        "drink": "Prefer hydration-supporting drinks over sweet beverages",
    }

    tips = [
        f"At {int(payload.profile.body_weight_kg)} kg, protein should stay intentional rather than incidental in the plate.",
        "The live score responds to each edit, so small changes like replacing the drink or add-on can lift the overall rating quickly.",
        goal_notes[payload.profile.goal],
    ]

    return PlatePlanResponse(
        score=score,
        summary="This is your current plate quality score based on how the selected sections work together for balance, satiety, hydration support, and energy stability.",
        target_split=target_split,
        optimized_plate=optimized_items,
        adjustments=adjustments,
        tips=tips,
    )
