from fastapi import FastAPI, status, HTTPException, Depends
from sqlalchemy.orm import Session
from response import TodoResponse
from schema.request import TodoCreateRequest, TodoUpdateRequest

app = FastAPI()

import models
from database.db_connection import engine, SessionFactory

models.Base.metadata.create_all(bind=engine)



def get_db():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()

@app.get("/todos", response_model=list[TodoResponse], status_code=status.HTTP_200_OK)
def get_todos_handler(session: Session = Depends(get_db)):
    # 1. 쿼리 객체 생성: 데이터를 조회하는 쿼리 객체를 생성
    query = session.query(models.Todo)
    
    # 2. 쿼리 실행: 쿼리 객체를 데이터베이스에 전달해 실제 쿼리를 실행 (내부적으로 SQL 쿼리 생성)
    todos = query.all()
    
    # 3. 결과 변환: 반환된 ORM 객체를 리스트로 변환하여 사용 (DB의 contents를 응답의 title로 매핑)
    result = [
        TodoResponse(id=todo.id, title=todo.contents, is_done=todo.is_done) 
        for todo in todos
    ]
    return result

@app.post("/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo_handler(body: TodoCreateRequest, session: Session = Depends(get_db)):
    # 1. ORM 객체(할 일 데이터) 생성
    new_todo = models.Todo(contents=body.title, is_done=body.is_done)
    
    # 2. 데이터베이스에 추가 및 커밋
    session.add(new_todo)
    session.commit()
    session.refresh(new_todo)  # 새로 생성된 ID 등 데이터 갱신
    
    # 3. 결과 반환
    return TodoResponse(id=new_todo.id, title=new_todo.contents, is_done=new_todo.is_done)

@app.patch("/todos/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
def update_todo_handler(todo_id: int, body: TodoUpdateRequest, session: Session = Depends(get_db)):
    todo = session.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
        
    if body.title is not None:
        todo.contents = body.title
    if body.is_done is not None:
        todo.is_done = body.is_done
        
    session.commit()
    session.refresh(todo)
    return TodoResponse(id=todo.id, title=todo.contents, is_done=todo.is_done)

@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo_handler(todo_id: int, session: Session = Depends(get_db)):
    todo = session.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
        
    session.delete(todo)
    session.commit()
    return None
