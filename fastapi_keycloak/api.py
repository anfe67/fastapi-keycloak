import arrow
from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel, Field

try:
    from .keycloak_integration import User, access_guard
    from .settings import get_settings
except ImportError:
    from keycloak_integration import User, access_guard
    from settings import get_settings

context = get_settings().context
guard_users = access_guard(context=context, roles=["user"])
router = APIRouter()


class CreateProcessSchema(BaseModel):
    business_date: str = Field(
        ..., description="Date for which to run the process."
    )

@router.get("/public")
async def get_public() -> dict:
    return {"message": "Anyone can see this"}

@router.get("/user")
async def user_endpoint(user: User = Depends(guard_users)) -> dict:
    return {"message": f"Hello User {user.username}"}


@router.get("/me/roles", response_model=list[str])
async def get_auth_check(
    current_user: User = Depends(guard_users),
) -> dict:
    return current_user.roles[context]
