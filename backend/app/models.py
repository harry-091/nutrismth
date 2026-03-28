from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


AgeGroup = Literal["13-17", "18-25", "26-40", "41-60", "60+"]
Gender = Literal["female", "male", "non-binary", "prefer_not_to_say"]
HydrationLevel = Literal["low", "medium", "high"]
MealPattern = Literal["irregular", "mixed", "balanced"]
ProduceFrequency = Literal["rarely", "sometimes", "daily"]
SnackPreference = Literal["packaged", "mixed", "whole_food"]


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
    water_intake_liters: float = Field(ge=0.2, le=8)
    hydration_level: HydrationLevel
    meal_pattern: MealPattern
    produce_frequency: ProduceFrequency
    snack_preference: SnackPreference
    sugary_drinks_per_week: int = Field(ge=0, le=35)
    activity_level: Literal["low", "moderate", "high"]


class AssessmentResponse(BaseModel):
    status: Literal["received"]
    normalized: AssessmentPayload
    score: int


class UserSummary(BaseModel):
    hydration_band: str
    meal_pattern_band: str
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
    hydration_recommendation: GuidanceCard
    plate_guidance: GuidanceCard
    smart_swaps: GuidanceCard
    nutrient_education: GuidanceCard


class ContentResponse(BaseModel):
    sections: list[ContentSection]


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
