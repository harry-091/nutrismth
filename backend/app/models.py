from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


AgeGroup = Literal["15-18", "19-25", "26-35", "35+"]
Gender = Literal["female", "male"]


class SectionHighlight(BaseModel):
    label: str
    value: str
    detail: str


class ContentSection(BaseModel):
    slug: str
    eyebrow: str
    title: str
    body: str
    highlights: list[SectionHighlight] = Field(default_factory=list)


class AssessmentPayload(BaseModel):
    age_group: AgeGroup
    gender: Gender
    diet_type: Literal["vegetarian", "non-vegetarian", "eggetarian", "vegan"]
    meals_per_day: Literal["1-2", "3", "4+"]
    fruit_veg_frequency: Literal["daily", "4-6_week", "1-3_week", "rarely"]
    diet_trend: Literal["none", "keto", "intermittent_fasting", "detox_cleanse", "gm_diet"]
    water_intake: Literal["lt_1", "1-2", "2-3", "gt_3"]
    carb_source: Literal["rice", "wheat", "potatoes", "fruits", "sweets", "processed", "other"]
    protein_source: Literal["pulses", "eggs", "dairy", "meat", "soy", "nuts", "other"]
    fat_source: Literal["oils", "ghee_butter", "nuts", "fried_foods", "dairy", "other"]
    post_carb_feeling: Literal["energetic", "normal", "sleepy_heavy"]
    breakfast_type: Literal["heavy", "quick", "south_indian", "tea_biscuits", "skip"]
    dinner_type: Literal["light", "balanced", "one_pot", "takeout"]
    goal_victory: Literal["more_energy", "better_sleep", "clearer_skin", "feeling_stronger", "no_afternoon_slump"]
    activity_level: Literal["low", "moderate", "high"]


class AssessmentResponse(BaseModel):
    status: Literal["received"]
    normalized: AssessmentPayload
    score: int


class UserSummary(BaseModel):
    hydration_band: str
    meal_rhythm_band: str
    nutrition_variety_band: str


class RiskIndicator(BaseModel):
    title: str
    level: Literal["low", "medium", "high"]
    description: str


class GuidanceCard(BaseModel):
    title: str
    summary: str
    actions: list[str]


class RecommendationResponse(BaseModel):
    user_summary: UserSummary
    score: int
    source: str
    confidence_note: str
    risk_indicators: list[RiskIndicator]
    suggested_plate: list["PlateItem"]
    hydration_recommendation: GuidanceCard
    plate_guidance: GuidanceCard
    smart_swaps: GuidanceCard
    nutrient_education: GuidanceCard


class ContentResponse(BaseModel):
    sections: list[ContentSection]


class ModelMetricsResponse(BaseModel):
    model_name: str
    training_source: str
    sample_count: int
    training_log: list[str]
    score_mae: float
    score_r2: float
    hydration_accuracy: float
    meal_rhythm_accuracy: float
    variety_accuracy: float
    plate_accuracy: dict[str, float]


PlateCategory = Literal["base", "protein", "vegetable", "side"]


class PlateItem(BaseModel):
    category: PlateCategory
    name: str


class PlateProfile(BaseModel):
    age_group: AgeGroup
    gender: Gender
    body_weight_kg: float = Field(ge=25, le=250)
    activity_level: Literal["low", "moderate", "high"]
    goal: Literal["balanced", "higher_protein", "lighter_meal", "energy_support"]


class PlatePlanRequest(BaseModel):
    items: list[PlateItem] = Field(min_length=3, max_length=4)
    profile: PlateProfile


class PlateSuggestion(BaseModel):
    category: PlateCategory
    original: str
    updated: str
    reason: str


class PlatePlanResponse(BaseModel):
    score: int
    summary: str
    target_split: dict[str, str]
    optimized_plate: list[PlateItem]
    adjustments: list[PlateSuggestion]
    tips: list[str]
