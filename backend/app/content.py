from .models import ContentSection, SectionHighlight


CONTENT_SECTIONS = [
    ContentSection(
        slug="problem",
        eyebrow="The challenge",
        title="Young diets are being shaped by convenience instead of balance.",
        body=(
            "The report frames nutrition as a practical, everyday systems problem. "
            "Hydration slips first, meal timing becomes inconsistent, and packaged "
            "foods crowd out nutrient-dense choices when routines get busy."
        ),
        highlights=[
            SectionHighlight(
                label="Focus",
                value="Hydration + balance",
                detail="The MVP starts with actions people can understand and follow daily.",
            ),
            SectionHighlight(
                label="Audience",
                value="Indian households",
                detail="Content and food swap ideas reflect locally familiar eating patterns.",
            ),
        ],
    ),
    ContentSection(
        slug="research",
        eyebrow="Research lens",
        title="A machine-learning product needs explainable habits before predictive depth.",
        body=(
            "The report argues for using machine learning to interpret survey patterns "
            "and turn them into useful guidance. This first version keeps the logic "
            "transparent with structured rules while preserving a clean upgrade path."
        ),
        highlights=[
            SectionHighlight(
                label="Current engine",
                value="Deterministic",
                detail="Recommendation categories are traceable and easy to validate.",
            ),
            SectionHighlight(
                label="Future path",
                value="Model-ready",
                detail="The API contract can accept a trained model later without UI rework.",
            ),
        ],
    ),
    ContentSection(
        slug="solution",
        eyebrow="Four response pillars",
        title="The platform translates research into hydration, plate design, smart swaps, and nutrient literacy.",
        body=(
            "Instead of a generic wellness dashboard, the site delivers focused, actionable "
            "guidance: drink enough water, build a balanced plate, swap refined items for "
            "stronger alternatives, and understand why micronutrients matter."
        ),
        highlights=[
            SectionHighlight(
                label="Hydration",
                value="Trackable habits",
                detail="Daily water goals are converted into routines people can actually remember.",
            ),
            SectionHighlight(
                label="Plate method",
                value="Simple visual rule",
                detail="A half-vegetable, quarter-protein, quarter-smart-carb model anchors the advice.",
            ),
            SectionHighlight(
                label="Swaps",
                value="Low-friction changes",
                detail="Millets, brown rice, seeds, fruit, and whole-food snacks reduce decision fatigue.",
            ),
        ],
    ),
]
