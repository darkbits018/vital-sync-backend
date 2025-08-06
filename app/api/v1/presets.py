from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.workout_preset import WorkoutPreset, WorkoutPresetCreate, WorkoutPresetUpdate, PresetExercise, \
    PresetSet
from app.db.session import get_db
from app.models.workout_preset import WorkoutPreset as WorkoutPresetModel
from app.models.preset_exercise import PresetExercise as PresetExerciseModel
from app.models.preset_set import PresetSet as PresetSetModel
from app.services.firebase_auth import get_current_user

router = APIRouter()


@router.get("/", response_model=list[WorkoutPreset])
async def read_presets(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    presets = db.query(WorkoutPresetModel).offset(skip).limit(limit).all()
    return presets


@router.get("/{preset_id}", response_model=WorkoutPreset)
async def read_preset(
        preset_id: str,
        db: Session = Depends(get_db)
):
    preset = db.query(WorkoutPresetModel).filter(WorkoutPresetModel.id == preset_id).first()
    if not preset:
        raise HTTPException(status_code=404, detail="Preset not found")
    return preset


@router.post("/", response_model=WorkoutPreset, status_code=status.HTTP_201_CREATED)
async def create_preset(
        preset: WorkoutPresetCreate,
        db: Session = Depends(get_db)
):
    db_preset = WorkoutPresetModel(
        id=preset.id,
        name=preset.name,
        category=preset.category,
        estimated_duration=preset.estimated_duration,
        estimated_calories=preset.estimated_calories
    )

    # Add exercises
    for exercise_data in preset.exercises:
        db_exercise = PresetExerciseModel(
            id=exercise_data.id,
            preset_id=db_preset.id,
            name=exercise_data.name,
            rest_time=exercise_data.rest_time,
            notes=exercise_data.notes
        )

        # Add sets
        for set_data in exercise_data.sets:
            db_set = PresetSetModel(
                id=set_data.id,
                exercise_id=db_exercise.id,
                set_number=set_data.set_number,
                reps=set_data.reps,
                weight=set_data.weight
            )
            db_exercise.sets.append(db_set)

        db_preset.exercises.append(db_exercise)

    db.add(db_preset)
    db.commit()
    db.refresh(db_preset)
    return db_preset


@router.put("/{preset_id}", response_model=WorkoutPreset)
async def update_preset(
        preset_id: str,
        preset_update: WorkoutPresetUpdate,
        db: Session = Depends(get_db)
):
    db_preset = db.query(WorkoutPresetModel).filter(WorkoutPresetModel.id == preset_id).first()

    if not db_preset:
        raise HTTPException(status_code=404, detail="Preset not found")

    # Update basic fields
    if preset_update.name is not None:
        db_preset.name = preset_update.name
    if preset_update.category is not None:
        db_preset.category = preset_update.category
    if preset_update.estimated_duration is not None:
        db_preset.estimated_duration = preset_update.estimated_duration
    if preset_update.estimated_calories is not None:
        db_preset.estimated_calories = preset_update.estimated_calories

    # Handle exercises (simplified - you might want more granular updates)
    if preset_update.exercises:
        # Clear existing exercises and sets
        for exercise in db_preset.exercises:
            db.delete(exercise)

        # Add updated exercises
        for exercise_data in preset_update.exercises:
            db_exercise = PresetExerciseModel(
                id=exercise_data.id,
                preset_id=db_preset.id,
                name=exercise_data.name,
                rest_time=exercise_data.rest_time,
                notes=exercise_data.notes
            )

            # Add sets
            for set_data in exercise_data.sets:
                db_set = PresetSetModel(
                    id=set_data.id,
                    exercise_id=db_exercise.id,
                    set_number=set_data.set_number,
                    reps=set_data.reps,
                    weight=set_data.weight
                )
                db_exercise.sets.append(db_set)

            db_preset.exercises.append(db_exercise)

    db.commit()
    db.refresh(db_preset)
    return db_preset


@router.delete("/{preset_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_preset(
        preset_id: str,
        db: Session = Depends(get_db)
):
    db_preset = db.query(WorkoutPresetModel).filter(WorkoutPresetModel.id == preset_id).first()

    if not db_preset:
        raise HTTPException(status_code=404, detail="Preset not found")

    db.delete(db_preset)
    db.commit()
    return {"message": "Preset deleted successfully"}
