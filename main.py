from fastapi import FastAPI, status
from response import TodoResponse

app = FastAPI()

# 임시 메모리 저장소 (테스트용)
todos_db = []

@app.get("/todos", response_model=list[TodoResponse], status_code=status.HTTP_200_OK)
def get_todos_handler():
    return todos_db
