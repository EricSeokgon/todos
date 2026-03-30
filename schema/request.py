from pydantic import BaseModel
from typing import Optional

class TodoCreateRequest(BaseModel):
    title: str
    is_done: bool = False

class TodoUpdateRequest(BaseModel):
    title: Optional[str] = None
    is_done: Optional[bool] = None
