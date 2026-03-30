from pydantic import BaseModel

class TodoCreateRequest(BaseModel):
    title: str
    is_done: bool = False
