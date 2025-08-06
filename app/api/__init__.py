from fastapi import APIRouter
from app.api.v1 import auth, users, workouts, presets, meals, medicines, preferences, macros, chat

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(workouts.router, prefix="/workouts", tags=["workouts"])
api_router.include_router(presets.router, prefix="/presets", tags=["presets"])
api_router.include_router(meals.router, prefix="/meals", tags=["meals"])
api_router.include_router(medicines.router, prefix="/medicines", tags=["medicines"])
api_router.include_router(preferences.router, prefix="/preferences", tags=["preferences"])
api_router.include_router(macros.router, prefix="/macros", tags=["macros"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])