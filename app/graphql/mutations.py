from datetime import datetime, timezone

from graphql import GraphQLError
import strawberry
from bson import ObjectId
from fastapi import HTTPException
import logging

from app.db import get_collection
from app.graphql.types import BlogResponseType, UserResponseType


LOGGER = logging.getLogger(name="MUTATION")

@strawberry.type
class Mutation:

    @strawberry.mutation
    async def create_user(
        self, username: str, email: str, password: str
    ) -> UserResponseType:

        if not email or not isinstance(email, str) or "@" not in email:
            raise ValueError("Invalid email. Please provide a valid email address.")

        if not password or not isinstance(password, str) or len(password) < 8:
            raise ValueError(
                "Invalid password. Password must be at least 8 characters long."
            )

        user_data = {"username": username, "email": email, "password": password}
        user_collection = get_collection("user")
        obj = await user_collection.insert_one(user_data)
        print("user_obj")
        print(obj)
        return UserResponseType(
            id=str(obj.inserted_id),
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"],
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

    @strawberry.mutation
    async def like_or_dislike(
        self, blog_id: str, value: int, field:str
    ) -> BlogResponseType:

        blog_collection = get_collection("blog")

        try:
            blog_obj_id = ObjectId(blog_id)
        except Exception:
            raise GraphQLError("Invalid blog ID format")

        blog_obj = await blog_collection.find_one({"_id": blog_obj_id})
        if not blog_obj:
            raise GraphQLError("BLOG WITH ID DOES NOT EXIST")

        # if blog_obj["like"] < 0 or blog_obj["dislike"] < 0:
        #     raise GraphQLError("Like/Dislike Can't be Negative")

        if value == -1 and blog_obj[field] == 0:
            LOGGER.info("No Decrement")
            return BlogResponseType(
                id=str(blog_obj["_id"]),
                user_id=blog_obj["user_id"],
                like=blog_obj["like"],
                dislike=blog_obj["dislike"],
                created_at=blog_obj["created_at"],
                content=blog_obj['content'],
            )

        # if value < 0 and (blog_obj["like"] >= 0 or blog_obj["dislike"] >= 0):
        updated_blog = await blog_collection.find_one_and_update(
            {"_id": blog_obj_id}, {"$inc": {field: value}}, return_document=True
        )

        return BlogResponseType(
            id=str(updated_blog["_id"]),
            user_id=updated_blog["user_id"],
            like=updated_blog["like"],
            dislike=updated_blog["dislike"],
            created_at=updated_blog["created_at"],
            content=updated_blog["content"],
        )
