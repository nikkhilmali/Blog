from datetime import datetime, timezone

from pydantic import BaseModel


class Blog(BaseModel):
    user_id: str
    content: str
    like: int
    dislike: int

    created_at: datetime = datetime.now(timezone.utc)
    update_at: datetime = datetime.now(timezone.utc)