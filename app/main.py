import dotenv

dotenv.load_dotenv()
from fastapi import FastAPI, Depends
from fastapi import FastAPI, Depends
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.meals import router as meals_router
from app.api.v1.macros import router as macros_router
from app.api.v1.medicines import router as medicines_router
from app.api.v1.preferences import router as preferences_router
from app.api.v1.presets import router as presets_router
from app.api.v1.workouts import router as workouts_router
from app.api.v1.chat import router as chat_router
from app.api.v1.analytics import router as analytics_router
from app.api.v1.notifications import router as notifications_router
from app.db.base import Base, meal_foods
from app.core.config import get_settings
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.sockets.manager import socket_app

settings = get_settings()

app = FastAPI(title="VitalSync Backend")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/ws", socket_app)


@app.get("/")
def read_root(db: Session = Depends(get_db)):
    return {"Hello": "Welcome to VitalSync Backend"}


app.include_router(auth_router, prefix="/api/v1", tags=["auth"])
app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
app.include_router(meals_router, prefix="/api/v1/meals", tags=["meals"])
app.include_router(macros_router, prefix="/api/v1/macros", tags=["macros"])
app.include_router(medicines_router, prefix="/api/v1/medicines", tags=["medicines"])
app.include_router(preferences_router, prefix="/api/v1/preferences", tags=["preferences"])
app.include_router(presets_router, prefix="/api/v1/presets", tags=["presets"])
app.include_router(workouts_router, prefix="/api/v1/workouts", tags=["workouts"])
app.include_router(chat_router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(analytics_router, prefix="/api/v1/analytics", tags=["analytics"])
app.include_router(notifications_router, prefix="/api/v1/notifications", tags=["notifications"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
