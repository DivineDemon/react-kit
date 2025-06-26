from fastapi import APIRouter, Depends, status
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants.utils import get_current_user
from app.core.db import get_db
from app.core.jwt import create_access_token
from app.models.user import User as ORMUser
from app.schemas.generic import ResponseModel
from app.schemas.user_schema import (
    UserBase,
    UserDelete,
    UserJWT,
    UserLogin,
    UserRead,
    UserUpdate,
)

router = APIRouter(prefix="/users", tags=["users"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", response_model=ResponseModel[UserRead])
async def register_user(user: UserBase, db: AsyncSession = Depends(get_db)):
    try:
        query = select(ORMUser).where(ORMUser.email == user.email)
        result = await db.execute(query)
        existing_user = result.scalar_one_or_none()

        if existing_user:
            return ResponseModel(
                data=None,
                status=status.HTTP_400_BAD_REQUEST,
                message="User with this email already exists."
            )

        hashed_password = pwd_context.hash(user.password)

        db_user = ORMUser(
            email=user.email,
            password=hashed_password,
            first_name=user.first_name,
            last_name=user.last_name,
            profile_picture=str(
                user.profile_picture) if user.profile_picture else None
        )

        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)

        return ResponseModel(
            status=status.HTTP_201_CREATED,
            data=UserRead.model_validate(db_user),
            message="User registered successfully."
        )
    except Exception as e:
        await db.rollback()

        return ResponseModel(
            data=None,
            message=str(e),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.post("/login", response_model=ResponseModel[UserRead])
async def login_user(user: UserLogin, db: AsyncSession = Depends(get_db)):
    try:
        query = select(ORMUser).where(ORMUser.email == user.email)
        result = await db.execute(query)
        db_user = result.scalar_one_or_none()

        if not db_user or \
            not pwd_context.verify(user.password, getattr(db_user, "password", None)):
            return ResponseModel(
                data=None,
                status=status.HTTP_401_UNAUTHORIZED,
                message="Invalid email or password."
            )

        token = create_access_token({"sub": db_user.email, "user_id": db_user.id})
        user_read = UserRead.model_validate(db_user)
        user_read.token = token

        return ResponseModel(
            data=user_read,
            status=status.HTTP_200_OK,
            message="Login successful."
        )
    except Exception as e:
        return ResponseModel(
            data=None,
            message=str(e),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.get("/me", response_model=ResponseModel[UserRead])
async def get_my_profile(db: AsyncSession = \
                         Depends(get_db), current_user: \
                            UserJWT = Depends(get_current_user)):
    try:
        query = select(ORMUser).where(ORMUser.id == current_user.user_id)
        result = await db.execute(query)
        db_user = result.scalar_one_or_none()

        if not db_user:
            return ResponseModel(
                data=None,
                status=status.HTTP_404_NOT_FOUND,
                message="User not found."
            )

        return ResponseModel(
            data=UserRead.model_validate(db_user),
            status=status.HTTP_200_OK,
            message="User profile retrieved successfully."
        )
    except Exception as e:
        return ResponseModel(
            data=None,
            message=str(e),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    

@router.put("/me", response_model=ResponseModel[UserRead])
async def update_user_profile(
    user: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserJWT = Depends(get_current_user)
):
    try:
        query = select(ORMUser).where(ORMUser.id == current_user.user_id)
        result = await db.execute(query)
        db_user = result.scalar_one_or_none()

        if not db_user:
            return ResponseModel(
                data=None,
                message="User not found.",
                status=status.HTTP_404_NOT_FOUND
            )

        if user.email and user.email != db_user.email:
            existing_query = select(ORMUser).where(ORMUser.email == user.email)
            existing_result = await db.execute(existing_query)
            existing_user = existing_result.scalar_one_or_none()
            if existing_user:
                return ResponseModel(
                    data=None,
                    message="Email already in use.",
                    status=status.HTTP_400_BAD_REQUEST
                )
            setattr(db_user, "email", user.email)

        if user.new_password:
            if not user.current_password:
                return ResponseModel(
                    data=None,
                    status=status.HTTP_400_BAD_REQUEST,
                    message="Current password is required to set a new password."
                )
            
            if not pwd_context.verify(user.current_password, \
                                      getattr(db_user, "password", None)):
                return ResponseModel(
                    data=None,
                    status=status.HTTP_400_BAD_REQUEST,
                    message="Current password is incorrect."
                )
            
            setattr(db_user, "password", pwd_context.hash(user.new_password))

        for attr in ["first_name", "last_name", "profile_picture"]:
            value = getattr(user, attr, None)
            if value is not None:
                setattr(db_user, attr, str(value) if attr ==
                        "profile_picture" else value)

        await db.commit()
        await db.refresh(db_user)

        return ResponseModel(
            data=UserRead.model_validate(db_user),
            status=status.HTTP_200_OK,
            message="User profile updated successfully."
        )
    except Exception as e:
        await db.rollback()
        return ResponseModel(
            data=None,
            message=str(e),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.delete("/me", response_model=ResponseModel[UserDelete])
async def delete_user_profile(
    db: AsyncSession = Depends(get_db),
    current_user: UserJWT = Depends(get_current_user)
):
    try:
        query = select(ORMUser).where(ORMUser.id == current_user.user_id)
        result = await db.execute(query)
        db_user = result.scalar_one_or_none()

        if not db_user:
            return ResponseModel(
                data=None,
                message="User not found.",
                status=status.HTTP_404_NOT_FOUND
            )

        await db.delete(db_user)
        await db.commit()

        return ResponseModel(
            status=status.HTTP_200_OK,
            data=UserDelete(id=current_user.user_id),
            message="User profile deleted successfully."
        )
    except Exception as e:
        await db.rollback()
        return ResponseModel(
            data=None,
            message=str(e),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )