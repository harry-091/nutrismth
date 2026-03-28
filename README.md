# NutriQuest

Interactive nutrition website with a React frontend and a FastAPI backend.

## Stack

- Frontend: React + Vite
- Backend: FastAPI
- Recommendation engine: rule-based scoring and plate optimization

## Local development

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend runs at `http://127.0.0.1:8000`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://127.0.0.1:5173`.

## API endpoints

- `GET /health`
- `GET /content/sections`
- `POST /assessment`
- `POST /recommendations`
- `POST /plate/optimize`

## Tests

```bash
cd backend
.venv/bin/python -m pytest
```

## Deployment

This repo is now set up to deploy as a single service:

- the frontend is built inside Docker
- the built frontend files are copied into the backend
- FastAPI serves the frontend from `backend/app/static`

Files added for deployment:

- `Dockerfile`
- `render.yaml`
- `.dockerignore`

### Render

1. Push this repo to GitHub.
2. Create a new Render Blueprint or Web Service from the repo.
3. Render will detect `render.yaml` or the `Dockerfile`.
4. Deploy.

### Docker

```bash
docker build -t nutriquest .
docker run -p 8000:8000 nutriquest
```

Then open `http://127.0.0.1:8000`.

## Documentation

Detailed system explanation:

- `docs/SYSTEM_GUIDE.md`

It creates the FastAPI app and exposes endpoints:

- `GET /health`
- `GET /content/sections`
- `POST /assessment`
- `POST /recommendations`
- `POST /plate/optimize`

### Why FastAPI is a good choice here

FastAPI is good for this kind of app because:

- it validates input automatically
- it works well with JSON APIs
- it is simple to structure
- it is future-friendly for ML model serving

## 6. Data Models

The data models live in:

- `models.py`

These models define what kind of data the backend accepts and returns.

### Survey models

The survey input model is `AssessmentPayload`.

It contains:

- `age_group`
- `gender`
- `water_intake_liters`
- `hydration_level`
- `meal_pattern`
- `produce_frequency`
- `snack_preference`
- `sugary_drinks_per_week`
- `activity_level`

The output models include:

- `AssessmentResponse`
- `RecommendationResponse`
- `UserSummary`
- `RiskIndicator`
- `GuidanceCard`

### Plate planner models

The plate planner uses:

- `PlateItem`
- `PlateProfile`
- `PlatePlanRequest`
- `PlateSuggestion`
- `PlatePlanResponse`

This separation is important because plate planning is not the same as survey scoring.

## 7. How the Survey Recommendation System Works

The main logic is in:

- `recommendations.py`

### Step 1: normalize input

The function `normalize_payload()` cleans the request a little.

Right now it mainly:

- rounds water intake

This is useful because:

- it makes data more consistent
- it reduces tiny input differences

### Step 2: compute a nutrition score

The function `compute_score()` gives the user a score between 0 and 100.

It starts with:

```python
score = 50
```

Then it adjusts that score based on habits.

Examples:

- more water increases the score
- irregular meals reduce the score
- daily produce increases the score
- packaged snacks reduce the score
- sugary drinks reduce the score
- higher activity can increase the score

So logically it behaves like this:

```text
final score
= base score
+ hydration bonus
+ meal quality bonus
+ produce bonus
+ snack quality bonus
+ activity bonus
- sugary drink penalty
```

Then the score is clamped between 0 and 100.

### Step 3: turn the score and habits into recommendations

The function `build_recommendations()` does not just return a number.

It builds a structured response including:

- user summary
- risk indicators
- hydration guidance
- plate guidance
- smart swaps
- nutrient education

This is important because the backend is not returning raw HTML.

It returns clean JSON, and the frontend decides how to display it.

That is a good design choice.

## 8. How the Plate Planner Works

The user-facing plate planner is in:

- `PlatePlannerSection.jsx`

### What the user does

The user:

1. Picks foods for:
   - base
   - protein
   - vegetable
   - side
2. Searches through options in each category
3. Enters:
   - age group
   - gender
   - body weight
   - activity level
   - goal
4. Submits the plate

### What the frontend sends

The frontend sends a JSON payload like:

```json
{
  "items": [
    { "category": "base", "name": "white rice" },
    { "category": "protein", "name": "dal" },
    { "category": "vegetable", "name": "sabzi" },
    { "category": "side", "name": "fruit" }
  ],
  "profile": {
    "age_group": "18-25",
    "gender": "female",
    "body_weight_kg": 60,
    "activity_level": "moderate",
    "goal": "balanced"
  }
}
```

### What the backend does

The backend calls:

- `optimize_plate()`

That function checks each selected food against `PLATE_LIBRARY`.

Each item in `PLATE_LIBRARY` has:

- an updated replacement
- a quality tag

Examples:

- `white rice -> brown rice`
- `soft drink -> water`
- `potato fries -> sauteed vegetables`
- `fried chicken -> grilled chicken`

### Important constraint

The backend only replaces foods with items that already exist in the allowed options.

That means:

- the user sees valid corrections
- the frontend and backend stay aligned
- the app never invents random foods outside the picker

This is a strong design decision.

## 9. What the Current ML Layer Actually Is

This section is important.

Right now the app is **not doing machine learning inference**.

It is doing:

- rule evaluation
- weighted scoring
- controlled replacements
- conditional response generation

This is closer to:

- an expert system
- a deterministic recommender

than to:

- a trained classifier
- a regression model
- a recommendation model

### Why people still call this "ML-like"

Because it behaves like an intelligent system from the user’s point of view:

- it collects features
- it processes inputs
- it produces personalized output

But from a technical point of view, it is not ML until it learns patterns from data.

## 10. What a Real ML Version Would Look Like

To convert this into a true ML project, you need data.

### What data you would need

For each user, you would want to store:

- age group
- gender
- body weight
- hydration inputs
- meal pattern
- produce frequency
- snack preference
- sugary drink count
- activity level
- plate selections
- goal
- recommendation shown
- whether the recommendation was accepted
- optional follow-up outcomes later

### Example dataset row

```text
age_group=18-25
gender=female
body_weight_kg=60
water_intake_liters=1.2
hydration_level=low
meal_pattern=irregular
produce_frequency=sometimes
snack_preference=packaged
sugary_drinks_per_week=6
activity_level=moderate
selected_base=white rice
selected_protein=fried chicken
selected_vegetable=none
selected_side=soft drink
goal=balanced
output_score=42
predicted_risk=high
recommended_base=brown rice
recommended_side=water
```

## 11. Possible ML Tasks in This Project

There are multiple possible ML problems here.

### 1. Risk classification

Goal:

- predict whether a user is low, medium, or high risk

Input:

- survey features

Output:

- class label

Possible models:

- logistic regression
- random forest
- XGBoost

### 2. Score prediction

Goal:

- predict a nutrition score directly

Input:

- survey and plate features

Output:

- numeric score

Possible models:

- linear regression
- gradient boosting regressor
- random forest regressor

### 3. Plate correction recommendation

Goal:

- suggest the best replacement item for each category

Input:

- chosen plate + profile

Output:

- best replacement candidate

Possible models:

- multiclass classification
- ranking model
- hybrid rule + ML approach

### 4. User segmentation

Goal:

- group users into habit clusters

Possible models:

- K-means
- hierarchical clustering

This can help create better recommendation groups later.

## 12. Recommended ML Design for This Project

The best real-world version is probably **hybrid ML**, not pure ML.

That means:

1. Use ML for prediction
2. Use rules for safety and validity

### Why hybrid is better

If you let a model generate plate recommendations completely freely, it may:

- produce inconsistent suggestions
- recommend unsupported foods
- recommend bad substitutions
- become hard to explain

Instead:

- let ML score or rank options
- then filter final outputs through business rules

Example:

```text
model ranks:
1. water
2. buttermilk
3. curd

rules check:
- is it in allowed options?
- does it fit the selected goal?
- is it a valid side item?

final output:
water
```

That is much safer.

## 13. How Someone Would Code the ML Version

Here is a practical step-by-step implementation plan.

### Step 1: store user interactions

Right now the app does not save user data permanently.

To build ML later, you should add a database.

Examples:

- PostgreSQL
- SQLite for prototype

You would save:

- survey submissions
- plate planner submissions
- returned recommendations
- user feedback if available

### Step 2: create a training pipeline

Create a new folder like:

```text
backend/ml/
```

Inside it, create:

- `prepare_data.py`
- `train_model.py`
- `evaluate_model.py`
- `predict.py`

### Step 3: prepare the data

In `prepare_data.py`, you would:

- load raw data
- clean invalid rows
- fill or remove missing values
- convert categories into numeric features
- split features and labels

### Step 4: encode categorical variables

Most ML models need numeric input.

So fields like:

- `meal_pattern`
- `goal`
- `snack_preference`
- `selected_base`

must be encoded.

Most likely you would use:

- one-hot encoding

### Step 5: train a baseline model

For example:

```python
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
```

Then:

1. define numeric columns
2. define categorical columns
3. build preprocessing pipeline
4. fit the model
5. evaluate on validation/test data
6. save model with `joblib`

### Step 6: save the trained model

You would save:

- the model
- the feature encoder/preprocessing pipeline

For example:

```python
import joblib
joblib.dump(model, "model.joblib")
joblib.dump(preprocessor, "preprocessor.joblib")
```

### Step 7: load the model in FastAPI

Then in the backend:

```python
import joblib

model = joblib.load("model.joblib")
preprocessor = joblib.load("preprocessor.joblib")
```

### Step 8: create an ML inference function

Something like:

```python
def predict_with_model(payload):
    row = payload_to_dict(payload)
    x = preprocessor.transform([row])
    prediction = model.predict(x)
    return prediction
```

### Step 9: combine ML with rules

Do not fully replace rules.

Use ML like this:

```text
raw prediction from model
-> validate against allowed options
-> apply nutrition constraints
-> build final response JSON
```

This is the most realistic version of how a production health-oriented system should work.

## 14. Why the Current Codebase Is Good for Future ML

This codebase is already set up in a useful way because:

- request models are separate from logic
- route handlers are thin
- logic is centralized in a service file
- frontend only depends on JSON contract

That means you can replace:

- internal scoring logic

without rewriting:

- the UI
- the page flow
- the form structure

This is one of the biggest strengths of the current architecture.

## 15. How to Code the Current Version From Scratch

If someone had to build the current project from nothing, the order would be:

### Backend

1. Create FastAPI app
2. Add CORS middleware
3. Define Pydantic models
4. Create content endpoint
5. Create assessment endpoint
6. Create recommendation logic
7. Create plate optimization logic
8. Add tests

### Frontend

1. Create React + Vite app
2. Build `App.jsx` state container
3. Add hash-based page switching
4. Build sections one by one
5. Add API helper functions
6. Connect survey to backend
7. Connect plate planner to backend
8. Style everything in CSS

## 16. How the Current Plate Logic Is Coded

The plate system is basically a controlled lookup-and-adjust model.

### Input

- user-selected foods
- user profile
- user goal

### Internal logic

For each food:

1. Find the item in `PLATE_LIBRARY`
2. Read its replacement and quality tag
3. Adjust score
4. Add explanation if a replacement happened
5. Build optimized plate output

### Output

- updated plate score
- target split
- optimized items
- explanations
- final tips

So this is not "generative AI". It is explicit structured decision logic.

## 17. If You Want a Stronger ML Project

Here is the most realistic upgrade path:

### Phase 1

- keep current rules
- save user interactions
- collect clean data

### Phase 2

- train a baseline classifier/regressor
- compare model outputs with current rule outputs

### Phase 3

- use model predictions for internal ranking
- keep rules as final filter

### Phase 4

- add explanation fields from feature importance
- add monitoring and retraining pipeline

## 18. Final Summary

This project currently works as a structured recommendation engine, not a trained ML system.

The frontend:

- handles page navigation
- shows forms and interactive flows
- renders results

The backend:

- validates requests
- computes survey scores
- builds recommendation cards
- optimizes meal plates

The current logic is rule-based, which is good for an MVP.

If you want true ML, the next big tasks are:

- collect real data
- define targets
- train models
- load them into FastAPI
- keep rules for safe final outputs

## 19. Useful Files to Read

If you want to understand the project by reading the code, start here:

- `frontend/src/App.jsx`
- `frontend/src/lib/api.js`
- `frontend/src/sections/PlatePlannerSection.jsx`
- `backend/app/main.py`
- `backend/app/models.py`
- `backend/app/services/recommendations.py`
- `backend/tests/test_api.py`
