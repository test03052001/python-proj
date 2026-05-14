from sqlalchemy.orm import Session

from app.models import AppUser
from app.repositories.users import UserRepository
from app.schemas.users import UserCreate, UserUpdate
from app.services.exceptions import ConflictError, NotFoundError


class UserService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.users = UserRepository(db)

    def list_users(self, offset: int = 0, limit: int = 100) -> list[AppUser]:
        return self.users.list(offset=offset, limit=limit)

    def get_user(self, user_id: int) -> AppUser:
        user = self.users.get(user_id)
        if user is None:
            raise NotFoundError("User not found")
        return user

    def create_user(self, payload: UserCreate) -> AppUser:
        if self.users.get_by_email(payload.email):
            raise ConflictError("A user with this email already exists")

        user = AppUser(email=payload.email, display_name=payload.display_name)
        self.users.add(user)
        self.db.commit()
        return user

    def update_user(self, user_id: int, payload: UserUpdate) -> AppUser:
        user = self.get_user(user_id)
        changes = payload.model_dump(exclude_unset=True)
        for field, value in changes.items():
            setattr(user, field, value)

        self.db.commit()
        self.db.refresh(user)
        return user

    def deactivate_user(self, user_id: int) -> AppUser:
        user = self.get_user(user_id)
        user.active = False
        self.db.commit()
        self.db.refresh(user)
        return user
