from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import create_access_token, decode_token, verify_password
from app.db.database import Base, engine, get_db
from app.models.user import User

router = APIRouter(prefix="/api/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# ---------- Schemas ----------

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class MeResponse(BaseModel):
    id: int
    email: EmailStr
    global_role: str

    model_config = {"from_attributes": True}


# ---------- Helpers ----------

def get_user_by_email(db: Session, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    return db.execute(stmt).scalars().first()


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    try:
        payload = decode_token(token)
        email = payload.get("sub")
        if not email:
            raise ValueError()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


# ---------- Routes ----------

@router.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # Swagger sends "username" field; we use it as email
    email = form_data.username
    password = form_data.password

    user = authenticate_user(db, email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(subject=user.email, global_role=user.global_role)
    return TokenResponse(access_token=token)


@router.get("/me", response_model=MeResponse)
def me(current_user: User = Depends(get_current_user)):
    return current_user
