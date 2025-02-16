import strawberry


@strawberry.type
class UserCreateType:
    username: str
    email: str
    password: str


@strawberry.type
class UserResponseType(UserCreateType):
    id: str


@strawberry.type
class UserLoginResponseType:
    id: str
    username:str
    email: str
    message:str
