from sqlalchemy import select

from app.models import AppUser
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[AppUser]):
    model = AppUser

    def get_by_email(self, email: str) -> AppUser | None:
        statement = select(AppUser).where(AppUser.email == email)
        return self.db.scalar(statement)
