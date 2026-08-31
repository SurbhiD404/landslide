from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login():
    """Phone + OTP login. Returns JWT on success."""
    return {"access_token": "mock-token", "token_type": "bearer"}
