from sqlalchemy.orm import Session
from app.models.meal import Meal as MealModel
from app.models.food import Food as FoodModel
from app.models.meal_food import MealFood as MealFoodModel
from app.schemas.meal import Meal, MealCreate, MealUpdate, Food, MealFood
from typing import List, Optional


def get_meals(db: Session, user_id: str, date: str = None, skip: int = 0, limit: int = 100) -> List[Meal]:
    query = db.query(MealModel).filter(MealModel.user_id == user_id)

    if date:
        query = query.filter(MealModel.date.like(f"{date}%"))

    return query.offset(skip).limit(limit).all()


def get_meal(db: Session, meal_id: str, user_id: str) -> Optional[Meal]:
    return db.query(MealModel).filter(
        MealModel.id == meal_id,
        MealModel.user_id == user_id
    ).first()


def create_meal(db: Session, meal: MealCreate, user_id: str) -> Meal:
    # Create meal
    db_meal = MealModel(**meal.dict(exclude={"foods"}), user_id=user_id)

    # Add foods
    for food_data in meal.foods:
        db_food = FoodModel(**food_data.dict(exclude={"quantity"}))
        db_food_entry = MealFoodModel(
            quantity=food_data.quantity
        )
        db_food_entry.food = db_food
        db_meal.foods.append(db_food_entry)

    db.add(db_meal)
    db.commit()
    db.refresh(db_meal)
    return db_meal


def update_meal(db: Session, meal_id: str, meal_update: MealUpdate, user_id: str) -> Optional[Meal]:
    db_meal = get_meal(db, meal_id, user_id)

    if not db_meal:
        return None

    # Update basic fields
    update_data = meal_update.dict(exclude_unset=True, exclude={"foods"})
    for key, value in update_data.items():
        setattr(db_meal, key, value)

    # Handle foods (simplified - you might want more granular updates)
    if meal_update.foods:
        # Clear existing foods
        for food_entry in db_meal.foods:
            db.delete(food_entry)

        # Add updated foods
        for food_data in meal_update.foods:
            db_food = FoodModel(**food_data.dict(exclude={"quantity"}))
            db_food_entry = MealFoodModel(
                quantity=food_data.quantity
            )
            db_food_entry.food = db_food
            db_meal.foods.append(db_food_entry)

    db.commit()
    db.refresh(db_meal)
    return db_meal


def delete_meal(db: Session, meal_id: str, user_id: str) -> bool:
    db_meal = get_meal(db, meal_id, user_id)

    if not db_meal:
        return False

    db.delete(db_meal)
    db.commit()
    return True
