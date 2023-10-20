from fastapi import FastAPI , HTTPException , Form
from typing import Optional , List
from pydantic import BaseModel

app = FastAPI(title="Todo API", description="A simple TODO API", version="1.0.0")

#class
class Todo(BaseModel):
    name:str
    due_date:str
    description:str

#creer une liste de todo
store_todo = []
print(store_todo)

#get
@app.get("/")
async def home():
    return {"Hello": "World"}

@app.post("/todo/")
async def create_todo_list(todo:Todo):
    store_todo.append(todo)
    return todo

@app.get("/todos/" , response_model=List[Todo])
async def get_todo_list():
    return store_todo

@app.get("/todo/{todo_id}")
async def get_todo_by_id(todo_id:int):
    try:
        return store_todo[todo_id]
    except:
        raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todo/{todo_id}")
async def delete_todo_by_id(todo_id:int):
    try:
        store_todo.pop(todo_id)
        return {"message":"Todo deleted successfully"}
    except:
        raise HTTPException(status_code=404, detail="Todo not found")

@app.put("/todo/{todo_id}")
async def update_todo_by_id(todo_id:int , todo:Todo):
    try:
        store_todo[todo_id] = todo
        return store_todo[todo_id]
    except:
        raise HTTPException(status_code=404, detail="Todo not found")

