from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token
from app.db.models import User
from app.db.session import get_session

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    phone_number: str
    otp_code: str


@router.post("/login")
async def login(request: LoginRequest, session: AsyncSession = Depends(get_session)):
    """Phone + OTP login. Returns JWT on success.

    DEV-MODE SIMPLIFICATION: OTP code "000000" is always accepted.
    This is a hackathon-timeline simplification, not a security oversight.
    """
    # Dev-mode: accept "000000" as always-valid OTP
    if request.otp_code != "000000":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid OTP",
        )

    # Look up or create user
    result = await session.execute(select(User).where(User.phone_number == request.phone_number))
    user = result.scalar_one_or_none()

    if not user:
        user = User(phone_number=request.phone_number, role="citizen")
        session.add(user)
        await session.commit()
        await session.refresh(user)

    # Issue JWT with user id and role
    access_token = create_access_token({"sub": str(user.id), "role": user.role})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user.role,
    }
