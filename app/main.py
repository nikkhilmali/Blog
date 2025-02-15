from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from app.schema import schema

app = FastAPI()


graphql_app = GraphQLRouter(schema=schema)
app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
async def root():
    return {"message": "Welcome to the Strawberry + FastAPI + MongoDB App!"}
