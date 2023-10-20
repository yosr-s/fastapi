from typing import List
from fastapi import FastAPI , HTTPException , Form , Request , Depends
from pydantic import BaseModel , Field
import databases
import sqlalchemy 
from datetime import datetime

DATABASE_URL="sqlite:///./db_test.db"

metadata = sqlalchemy.MetaData()

database=databases.Database(DATABASE_URL)

register = sqlalchemy.Table(
    "register",
    metadata,
    sqlalchemy.Column("id",sqlalchemy.Integer,primary_key=True),
    sqlalchemy.Column("name",sqlalchemy.String(50)),
    sqlalchemy.Column("date_created",sqlalchemy.DateTime())
)

engine = sqlalchemy.create_engine(
    DATABASE_URL,connect_args={"check_same_thread":False}
)

metadata.create_all(engine)
app=FastAPI()

@app.on_event("startup")
async def connect():
    await database.connect()

@app.on_event("shutdown")
async def disconnect():
    await database.disconnect()

class Register(BaseModel):
    id: int
    name:str
    date_created:datetime

class RegisterIn(BaseModel):
    name:str = Field(...)

@app.post("/register/" , response_model=Register)
async def create(r: RegisterIn=Depends()):
    query = register.insert().values(
        name=r.name,
        date_created=datetime.utcnow()
    )
    record_id = await database.execute(query)
    query = register.select().where(register.c.id == record_id)    
    row = await database.fetch_one(query)
    return {**row}

@app.get("/register/{id}" , response_model=Register)
async def get_one(id:int):
    query=register.select().where(register.c.id == id)
    user=await database.fetch_one(query)
    return {**user}

@app.get("/register/" , response_model=List[Register])
async def get_all():
    query=register.select()
    users=await database.fetch_all(query)
    return users

@app.delete("/register/{id}")
async def delete_one(id:int):
    query=register.delete().where(register.c.id == id)
    await database.execute(query)
    return {"message":"User deleted successfully"}

@app.put("/register/{id}" , response_model=Register)
async def update_one(id:int , r: RegisterIn=Depends()):
    query=register.update().where(register.c.id == id).values(
        name=r.name,
        date_created=datetime.utcnow()
    )
    await database.execute(query)
    query=register.select().where(register.c.id == id)
    user=await database.fetch_one(query)
    return {**user} 
