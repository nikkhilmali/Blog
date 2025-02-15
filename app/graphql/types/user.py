import strawberry


@strawberry.type
class UserCreateType:
    username: str
    email: str
    password: str


@strawberry.type
class UserResponseType(UserCreateType):
    id: str
