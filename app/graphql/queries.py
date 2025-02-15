from typing import List

import strawberry
import strawberry.file_uploads

from app.db import get_collection
from app.graphql.types import BlogResponseType, UserResponseType


@strawberry.type
class Query():
    """"""
    @strawberry.field
    async def users(self) -> List[UserResponseType]:
        """"""  
        user_collection = get_collection("user")
        users = await user_collection.find().to_list(100)
        print(users)
        return [
            UserResponseType(
                id=str(user['_id']),
                username=user["username"],
                email=user["email"],
                password=user["password"],
            )
            for user in users
        ]

    @strawberry.field
    async def blog(self) -> List[BlogResponseType]:
        """"""
        blog_collection = get_collection("blog")
        blogs = await blog_collection.find().to_list(100)
        print(blogs)
        return [
            BlogResponseType(
                id=str(blog.get("_id")),
                user_id=blog.get("user_id"),
                content=blog.get("content"),
                like=blog.get("like"),
                dislike=blog.get("dislike"),
                created_at=blog.get("created_at"),
            )
            for blog in blogs
        ]
