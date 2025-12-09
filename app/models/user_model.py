from pydantic import BaseModel

class User(BaseModel):
    id: int
    user: str
    email: str

class userResponse(BaseModel):
    status: str = "success"
    data: list[User]