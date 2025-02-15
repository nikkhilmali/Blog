from datetime import datetime, timezone

import strawberry
from bson import ObjectId
from fastapi import HTTPException

from app.db import get_collection
from app.graphql.types import BlogResponseType, UserResponseType


@strawberry.type
class Mutation:

    @strawberry.mutation
    async def create_user(
        self, username: str, email: str, password: str
    ) -> UserResponseType:

        if not email or not isinstance(email, str) or "@" not in email:
            raise ValueError("Invalid email. Please provide a valid email address.")

        if not password or not isinstance(password, str) or len(password) < 8:
            raise ValueError("Invalid password. Password must be at least 8 characters long.")

        user_data = {"username": username, "email": email, "password": password}
        user_collection = get_collection("user")
        obj = await user_collection.insert_one(user_data)
        print("user_obj")
        print(obj)
        return UserResponseType(
            id=str(obj.inserted_id),
            username=user_data["username"],
            email=user_data["email"],
            password=user_data[
                "password"
            ],
        )

    @strawberry.mutation
    async def create_blog(self, user_id: str, content: str) -> BlogResponseType:
        blog_data = {
            "user_id": user_id,
            "content": content,
            "like": 0,
            "dislike": 0,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }
        blog_collection = get_collection("blog")
        obj = await blog_collection.insert_one(blog_data)
        print("blog_obj")
        print(obj)
        return BlogResponseType(
            id=str(obj.inserted_id),
            user_id=blog_data["user_id"],
            like=blog_data["like"],
            dislike=blog_data["dislike"],
            created_at=blog_data["created_at"],
            content=blog_data["content"],
        )

    # @strawberry.mutation
    
    # async def like_or_dislike(
    #     self, blog_id: str, operation: str, like: int = 1, dislike: bool = False
    # ) -> BlogResponseType:
    #     blog_collection = get_collection("blog")

    #     blog = ObjectId(blog_id)

    #     value = 1 if operation == "inc" else -1

    #     obj = await blog_collection.find_one({"_id": blog})

    #     if like and obj['like'] and operation=='inc':
    #         await blog_collection.find_one_and_update(
    #             {"_id": blog, "like": {"$gte": 0}}, {"$inc": {"like": value}}
    #         )


    #     if dislike and obj['dislike'] and operation=='inc':
    #         await blog_collection.find_one_and_update(
    #             {"_id": blog, "dislike": {"$gte": 0}}, {"$inc": {"dislike": value}}
    #         )
            

    #     obj = await blog_collection.find_one({"_id": blog})

    #     return BlogResponseType(
    #         id=str(obj['_id']),
    #         user_id=obj["user_id"],
    #         like=obj["like"],
    #         dislike=obj["dislike"],
    #         created_at=obj["created_at"],
    #         content=obj["content"],
    #     )
