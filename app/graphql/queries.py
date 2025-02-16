from typing import List

from bson import ObjectId
import strawberry
import strawberry.file_uploads

from app.db import get_collection
from app.graphql.types import UserResponseType, BlogHomeResponseType


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
    async def blog(self) -> List[BlogHomeResponseType]:
        """"""
        blog_collection = get_collection("blog")
        user_collection = get_collection("user")
        blogs = await blog_collection.find().to_list(100)
        print(blogs)
        blog_list = []
        for blog in blogs:
            user = await user_collection.find_one(
                {"_id": ObjectId(blog["user_id"])}
            )
            if not user:
                user = {'username':"dummy"}
                
            blog_list.append(
                BlogHomeResponseType(
                    id=str(blog.get("_id")),
                    user_id=blog.get("user_id"),
                    username=user["username"],
                    content=blog.get("content"),
                    like=blog.get("like"),
                    dislike=blog.get("dislike"),
                    created_at=blog.get("created_at"),
                )
            )

        return blog_list
        # return [
        #     BlogResponseType(
        #         id=str(blog.get("_id")),
        #         user_id=blog.get("user_id"),
        #         content=blog.get("content"),
        #         like=blog.get("like"),
        #         dislike=blog.get("dislike"),
        #         created_at=blog.get("created_at"),
        #     )
        #     for blog in blogs
        # ]
