from datetime import datetime, timezone

from pydantic import UUID4, BaseModel


class User(BaseModel):
    id: UUID4
    username: str
    email: str
    password: str

    created_at: datetime = datetime.now(timezone.utc)
    update_at: datetime = datetime.now(timezone.utc)
