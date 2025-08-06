from sqlalchemy.orm import Session
from app.models.workout import Workout as WorkoutModel
from app.models.exercise import Exercise as ExerciseModel
from app.models.set import Set as SetModel
from app.schemas.workout import Workout, WorkoutCreate, WorkoutUpdate, Exercise, Set
from typing import List, Optional


def get_workouts(db: Session, user_id: str, skip: int = 0, limit: int = 100) -> List[Workout]:
    return db.query(WorkoutModel).filter(WorkoutModel.user_id == user_id).offset(skip).limit(limit).all()


def get_workout(db: Session, workout_id: str, user_id: str) -> Optional[Workout]:
    return db.query(WorkoutModel).filter(
        WorkoutModel.id == workout_id,
        WorkoutModel.user_id == user_id
    ).first()


def create_workout(db: Session, workout: WorkoutCreate, user_id: str) -> Workout:
    # Create workout
    db_workout = WorkoutModel(**workout.dict(exclude={"exercises"}), user_id=user_id)

    # Add exercises
    for exercise_data in workout.exercises:
        db_exercise = ExerciseModel(**exercise_data.dict(exclude={"sets"}))

        # Add sets to exercise
        for set_data in exercise_data.sets:
            db_set = SetModel(**set_data.dict())
            db_exercise.sets.append(db_set)

        db_workout.exercises.append(db_exercise)

    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout


def update_workout(db: Session, workout_id: str, workout_update: WorkoutUpdate, user_id: str) -> Optional[Workout]:
    db_workout = get_workout(db, workout_id, user_id)

    if not db_workout:
        return None

    # Update basic fields
    update_data = workout_update.dict(exclude_unset=True, exclude={"exercises"})
    for key, value in update_data.items():
        setattr(db_workout, key, value)

    # Handle exercises (simplified - you might want more granular updates)
    if workout_update.exercises:
        # Clear existing exercises and sets
        for exercise in db_workout.exercises:
            db.delete(exercise)

        # Add updated exercises
        for exercise_data in workout_update.exercises:
            db_exercise = ExerciseModel(**exercise_data.dict(exclude={"sets"}))

            # Add sets
            for set_data in exercise_data.sets:
                db_set = SetModel(**set_data.dict())
                db_exercise.sets.append(db_set)

            db_workout.exercises.append(db_exercise)

    db.commit()
    db.refresh(db_workout)
    return db_workout


def delete_workout(db: Session, workout_id: str, user_id: str) -> bool:
    db_workout = get_workout(db, workout_id, user_id)

    if not db_workout:
        return False

    db.delete(db_workout)
    db.commit()
    return True
