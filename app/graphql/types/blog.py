from datetime import datetime

import strawberry


@strawberry.type
class BlogCreateType:
    user_id: str
    content: str


@strawberry.type
class BlogResponseType(BlogCreateType):
    id:str
    like: int
    dislike: int
    created_at: datetime
