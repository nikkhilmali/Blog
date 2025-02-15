import strawberry


@strawberry.type
class ValidationError:
    field: str
    message: str
