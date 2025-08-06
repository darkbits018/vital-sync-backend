from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.auth import SignupRequest, UserResponse
from app.services.firebase_auth import verify_firebase_token
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserInDB
from datetime import datetime

router = APIRouter()


@router.post("/signup", response_model=UserResponse)
def signup_with_firebase(
        request: SignupRequest,
        db: Session = Depends(get_db),
        current_user_data: dict = Depends(verify_firebase_token)
):
    try:
        # Extract user data from Firebase
        firebase_uid = current_user_data["uid"]
        email = current_user_data.get("email", request.email)
        name = current_user_data.get("name", request.name)
        email_verified = current_user_data.get("email_verified", False)

        # Check if user already exists
        user = db.query(User).filter(User.id == firebase_uid).first()

        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists"
            )

        # Create new user with onboarding data
        user = User(
            id=firebase_uid,
            username=request.username,
            email=email,
            name=name,
            email_verified=email_verified,
            height=request.height,
            weight=request.weight,
            age=request.age,
            gender=request.gender,
            goal=request.goal,
            activity_level=request.activity_level,
            created_at=datetime.utcnow()
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        # Convert user object to response model
        user_response = UserInDB.model_validate(user)

        return UserResponse(user=user_response)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Signup failed: {str(e)}"
        )


@router.post("/login", response_model=UserResponse)
def login_with_firebase(
        db: Session = Depends(get_db),
        current_user_data: dict = Depends(verify_firebase_token)
):
    try:
        # Extract user data from Firebase
        firebase_uid = current_user_data["uid"]
        email = current_user_data.get("email")
        name = current_user_data.get("name")
        email_verified = current_user_data.get("email_verified", False)

        # Check if user exists in local DB
        user = db.query(User).filter(User.id == firebase_uid).first()

        if not user:
            # Create new user with default onboarding data (for login without signup)
            user = User(
                id=firebase_uid,
                username=email.split("@")[0],  # Default username from email
                email=email,
                name=name or "User",
                email_verified=email_verified,
                height=175,
                weight=70,
                age=25,
                gender="other",
                goal="maintain",
                activity_level="moderate",
                created_at=datetime.utcnow()
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        # Convert user object to response model
        user_response = UserInDB.model_validate(user)

        return UserResponse(user=user_response)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )
