from fastapi import FastAPI, status
from response import TodoResponse
from schema.request import TodoCreateRequest

app = FastAPI()

# 임시 메모리 저장소 (테스트용)
todos_db = []

@app.get("/todos", response_model=list[TodoResponse], status_code=status.HTTP_200_OK)
def get_todos_handler():
    return todos_db

@app.post("/todos", status_code=status.HTTP_201_CREATED)
def create_todo_handler(body: TodoCreateRequest):
    new_todo = {
        "id": len(todos_db) + 1,
        "title": body.title,
        "is_done": body.is_done
    }
    todos_db.append(new_todo)
    return new_todo
