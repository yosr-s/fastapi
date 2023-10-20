from fastapi import FastAPI , HTTPException , Form
from models import Todo , Todo_Pydantic , TodoIn_Pydantic
from tortoise.contrib.fastapi import HTTPNotFoundError , register_tortoise
from pydantic import BaseModel

class Message(BaseModel):
    message:str

app=FastAPI(title="Todo API", description="A simple TODO API", version="1.0.0")

@app.get("/")
async def home():
    return {"Hello": "World"}

@app.post("/todo/",response_model=Todo_Pydantic)
async def create_todo_list(todo:TodoIn_Pydantic):
    todo_obj = await Todo.create(**todo.dict(exclude_unset=True))
    return await Todo_Pydantic.from_tortoise_orm(todo_obj)

@app.get("/todo/{id}" , response_model=TodoIn_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def get_one(id:int):
    return await TodoIn_Pydantic.from_queryset_single(Todo.get(id=id)) 

@app.get("/todos/" , response_model=list[TodoIn_Pydantic])
async def get_all():
    return await TodoIn_Pydantic.from_queryset(Todo.all())

@app.delete("/todo/{id}" , response_model=Message, responses={404: {"model": HTTPNotFoundError}})
async def delete_one(id:int):
    deleted_count = await Todo.filter(id=id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Todo {id} not found")
    return Message(message=f"Deleted todo {id}")

@app.put("/todo/{id}" , response_model=TodoIn_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def update_one(id:int , todo:TodoIn_Pydantic):
    await Todo.filter(id=id).update(**todo.dict(exclude_unset=True))
    return await TodoIn_Pydantic.from_queryset_single(Todo.get(id=id))

    


#configuration de la base de donnees
register_tortoise(
    app,
    db_url="sqlite://store.db",
    modules={"models":["models"]},
    generate_schemas=True,
    add_exception_handlers=True
)