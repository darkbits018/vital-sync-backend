from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.workout import Workout, WorkoutCreate, WorkoutUpdate, Exercise, Set
from app.db.session import get_db
from app.models.workout import Workout as WorkoutModel
from app.models.exercise import Exercise as ExerciseModel
from app.models.set import Set as SetModel
from app.services.firebase_auth import get_current_user

router = APIRouter()


@router.get("/", response_model=list[Workout])
async def read_workouts(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    workouts = db.query(WorkoutModel).filter(WorkoutModel.user_id == current_user["uid"]).offset(skip).limit(
        limit).all()
    return workouts


@router.get("/{workout_id}", response_model=Workout)
async def read_workout(
        workout_id: str,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    workout = db.query(WorkoutModel).filter(
        WorkoutModel.id == workout_id,
        WorkoutModel.user_id == current_user["uid"]
    ).first()

    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout


@router.post("/", response_model=Workout, status_code=status.HTTP_201_CREATED)
async def create_workout(
        workout: WorkoutCreate,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    # Create new workout
    db_workout = WorkoutModel(
        id=workout.id,
        user_id=current_user["uid"],
        name=workout.name,
        start_time=workout.start_time,
        notes=workout.notes,
        is_template=workout.is_template
    )

    # Add exercises
    for exercise_data in workout.exercises:
        db_exercise = ExerciseModel(
            id=exercise_data.id,
            workout_id=db_workout.id,
            name=exercise_data.name,
            rest_time=exercise_data.rest_time,
            notes=exercise_data.notes
        )

        # Add sets
        for set_data in exercise_data.sets:
            db_set = SetModel(
                id=set_data.id,
                exercise_id=db_exercise.id,
                set_number=set_data.set_number,
                reps=set_data.reps,
                weight=set_data.weight,
                completed=set_data.completed
            )
            db_exercise.sets.append(db_set)

        db_workout.exercises.append(db_exercise)

    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout


@router.put("/{workout_id}", response_model=Workout)
async def update_workout(
        workout_id: str,
        workout_update: WorkoutUpdate,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    db_workout = db.query(WorkoutModel).filter(
        WorkoutModel.id == workout_id,
        WorkoutModel.user_id == current_user["uid"]
    ).first()

    if not db_workout:
        raise HTTPException(status_code=404, detail="Workout not found")

    # Update basic fields
    if workout_update.name is not None:
        db_workout.name = workout_update.name
    if workout_update.start_time is not None:
        db_workout.start_time = workout_update.start_time
    if workout_update.end_time is not None:
        db_workout.end_time = workout_update.end_time
    if workout_update.duration is not None:
        db_workout.duration = workout_update.duration
    if workout_update.notes is not None:
        db_workout.notes = workout_update.notes
    if workout_update.is_template is not None:
        db_workout.is_template = workout_update.is_template

    # Handle exercises (simplified - you might want more granular updates)
    if workout_update.exercises:
        # Clear existing exercises and sets
        for exercise in db_workout.exercises:
            db.delete(exercise)

        # Add updated exercises
        for exercise_data in workout_update.exercises:
            db_exercise = ExerciseModel(
                id=exercise_data.id,
                workout_id=db_workout.id,
                name=exercise_data.name,
                rest_time=exercise_data.rest_time,
                notes=exercise_data.notes
            )

            # Add sets
            for set_data in exercise_data.sets:
                db_set = SetModel(
                    id=set_data.id,
                    exercise_id=db_exercise.id,
                    set_number=set_data.set_number,
                    reps=set_data.reps,
                    weight=set_data.weight,
                    completed=set_data.completed
                )
                db_exercise.sets.append(db_set)

            db_workout.exercises.append(db_exercise)

    db.commit()
    db.refresh(db_workout)
    return db_workout


@router.delete("/{workout_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workout(
        workout_id: str,
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    db_workout = db.query(WorkoutModel).filter(
        WorkoutModel.id == workout_id,
        WorkoutModel.user_id == current_user["uid"]
    ).first()

    if not db_workout:
        raise HTTPException(status_code=404, detail="Workout not found")

    db.delete(db_workout)
    db.commit()
    return {"message": "Workout deleted successfully"}
