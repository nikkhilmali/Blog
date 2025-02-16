import logging
import re
from datetime import datetime, timezone

import strawberry
from bson import ObjectId
from graphql import GraphQLError

from app.db import get_collection
from app.graphql.types import (BlogResponseType, UserLoginResponseType,
                               UserResponseType)

LOGGER = logging.getLogger(name="MUTATION")

@strawberry.type
class Mutation:

    @strawberry.mutation
    async def create_user(
        self, username: str, email: str, password: str
    ) -> UserResponseType:

        user_data = {"username": username, "email": email, "password": password}
        user_collection = get_collection("user")

        # user = 
        if await user_collection.find_one({"username":username}):
            raise GraphQLError("Username is already Take")

        if await user_collection.find_one({"email": email}):
            raise GraphQLError("Already Registred, Kindly Login")

        username_regex = r"^(?!.*\.\.)[a-zA-Z0-9._]{1,30}$"
        if not username or not isinstance(username, str) or not re.match(username_regex, username) or username.startswith('.') or username.endswith('.'):
            raise ValueError(
                "Invalid username. It must be 1-30 characters long, can contain letters, numbers, underscores, and periods, but cannot start/end with a period or have consecutive periods."
            )

        if not email or not isinstance(email, str) or "@" not in email:
            raise ValueError("Invalid email. Please provide a valid email address.")

        if not password or not isinstance(password, str) or len(password) < 8:
            raise ValueError(
                "Invalid password. Password must be at least 8 characters long."
            )

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
            raise GraphQLError("Not Found, Invalid blog ID")

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

    @strawberry.mutation
    async def login(self, username:str, password:str)->UserLoginResponseType:
        user_collection = get_collection("user")

        field = "username"

        if '@' in username:
            field = "email"

        user_obj = await user_collection.find_one({field: username})

        if not user_obj:
            raise GraphQLError("USER WITH USERNAME DOES NOT EXIST !")

        if password != user_obj.get("password"):
            raise ValueError("Incorrect Password !!, Try Again....")

        return UserLoginResponseType(
            id=user_obj.get("_id"),
            username=user_obj.get("username"),
            email=user_obj.get("email"),
            message="Login Successful !!"
        )
