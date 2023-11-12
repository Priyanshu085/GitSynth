from pydantic import BaseModel
from typing import List

class User(BaseModel):
    id: int
    name: str
    access_token: str
    repositories: List[str] = []
    