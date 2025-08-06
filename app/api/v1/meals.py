from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.meal import Meal, MealCreate, MealUpdate
from app.db.session import get_db
from app.models.meal import Meal as MealModel
from app.models.food import Food as FoodModel
from app.services.firebase_auth import get_current_user

router = APIRouter()


@router.get("/", response_model=list[Meal])
async def read_meals(
        date: str = None,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    query = db.query(MealModel).filter(MealModel.user_id == current_user["uid"])

    if date:
        query = query.filter(MealModel.date.like(f"{date}%"))

    meals = query.offset(skip).limit(limit).all()
    return meals


@router.get("/{meal_id}", response_model=Meal)
async def read_meal(
        meal_id: str,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    meal = db.query(MealModel).filter(
        MealModel.id == meal_id,
        MealModel.user_id == current_user["uid"]
    ).first()

    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    return meal


@router.post("/", response_model=Meal, status_code=status.HTTP_201_CREATED)
async def create_meal(
        meal: MealCreate,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    # Create new meal
    db_meal = MealModel(
        id=meal.id,
        user_id=current_user["uid"],
        name=meal.name,
        meal_type=meal.meal_type,
        date=meal.date,
        created_at=meal.created_at  # Ensure created_at is included if in schema
    )

    # Add foods using the meal_foods association table
    for food_data in meal.foods:  # Assuming foods is a list of {food_id, quantity}
        db_food = db.query(FoodModel).filter(FoodModel.id == food_data.food_id).first()
        if not db_food:
            raise HTTPException(status_code=404, detail=f"Food {food_data.food_id} not found")
        db_meal.foods.append(db_food)  # Associate food with meal
        # Store quantity in meal_foods (if needed, handled via custom logic or additional table attributes)

    db.add(db_meal)
    db.commit()
    db.refresh(db_meal)
    return db_meal


@router.put("/{meal_id}", response_model=Meal)
async def update_meal(
        meal_id: str,
        meal_update: MealUpdate,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    db_meal = db.query(MealModel).filter(
        MealModel.id == meal_id,
        MealModel.user_id == current_user["uid"]
    ).first()

    if not db_meal:
        raise HTTPException(status_code=404, detail="Meal not found")

    # Update basic fields
    if meal_update.name is not None:
        db_meal.name = meal_update.name
    if meal_update.meal_type is not None:
        db_meal.meal_type = meal_update.meal_type
    if meal_update.date is not None:
        db_meal.date = meal_update.date

    # Handle foods
    if meal_update.foods is not None:
        # Clear existing foods
        db_meal.foods.clear()
        # Add updated foods
        for food_data in meal_update.foods:
            db_food = db.query(FoodModel).filter(FoodModel.id == food_data.food_id).first()
            if not db_food:
                raise HTTPException(status_code=404, detail=f"Food {food_data.food_id} not found")
            db_meal.foods.append(db_food)  # Associate food with meal

    db.commit()
    db.refresh(db_meal)
    return db_meal


@router.delete("/{meal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_meal(
        meal_id: str,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    db_meal = db.query(MealModel).filter(
        MealModel.id == meal_id,
        MealModel.user_id == current_user["uid"]
    ).first()

    if not db_meal:
        raise HTTPException(status_code=404, detail="Meal not found")

    db.delete(db_meal)
    db.commit()
    return {"message": "Meal deleted successfully"}
