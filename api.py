from fastapi import FastAPI , HTTPException , Form  
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

#class
class CoordIn(BaseModel):
    password:str
    lat: float
    lon: float
    zoom:Optional[int]=None
    description:Optional[str]=None

class CoordOut(BaseModel):
    lat: float
    lon: float
    zoom:Optional[int]=None
    description:Optional[str]=None


@app.post("/position/", response_model=CoordOut, response_model_include={"description"})
async def make_position(coord:CoordIn):
    #db write done
    return coord

#get
@app.get("/")
async def hello_world():
    return {"Hello": "World"}

@app.get("/component/{component_id}")
async def get_component(component_id: int):
    return {"component_id": component_id}

@app.get("/component/")
async def read_component(number:int,text:Optional[str]):
    return {"number":number,"text":text}


#formData
@app.post("/login/")
async def login(username:str=Form(...),password:str=Form(...)):
    return {"username":username}  



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1" , port=8000)



