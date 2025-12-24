from fastapi import Depends, HTTPException, status

from app.models.user import User
from app.routers.auth_router import get_current_user


def require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.global_role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return current_user
