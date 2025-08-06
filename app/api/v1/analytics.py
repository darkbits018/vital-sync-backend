from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.firebase_auth import get_current_user
from app.models.workout import Workout
from app.models.meal import Meal
from app.models.macro_target import MacroTarget
from datetime import datetime
from typing import List
from pydantic import BaseModel

router = APIRouter()


class AnalyticsSummary(BaseModel):
    total_calories_burned: int
    total_workouts: int
    total_meals: int
    calorie_intake: int
    protein_intake: float
    carbs_intake: float
    fat_intake: float


@router.get("/summary", response_model=AnalyticsSummary)
async def get_analytics_summary(
        start_date: str,
        end_date: str,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    """Retrieve a summary of user fitness data for a date range.

    Args:
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.

    Returns:
        AnalyticsSummary: Summary of workouts and meals.
    """
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    # Workouts
    workouts = db.query(Workout).filter(
        Workout.user_id == current_user["uid"],
        Workout.start_time >= start,
        Workout.start_time <= end
    ).all()
    total_calories_burned = sum(w.duration or 0 for w in workouts) * 5  # Simplified calorie estimation
    total_workouts = len(workouts)

    # Meals
    meals = db.query(Meal).filter(
        Meal.user_id == current_user["uid"],
        Meal.date >= start,
        Meal.date <= end
    ).all()
    total_meals = len(meals)
    calorie_intake = sum(sum(f.food.calories * f.quantity for f in m.foods) for m in meals)
    protein_intake = sum(sum(f.food.protein * f.quantity for f in m.foods) for m in meals)
    carbs_intake = sum(sum(f.food.carbs * f.quantity for f in m.foods) for m in meals)
    fat_intake = sum(sum(f.food.fat * f.quantity for f in m.foods) for m in meals)

    return AnalyticsSummary(
        total_calories_burned=total_calories_burned,
        total_workouts=total_workouts,
        total_meals=total_meals,
        calorie_intake=calorie_intake,
        protein_intake=protein_intake,
        carbs_intake=carbs_intake,
        fat_intake=fat_intake
    )
