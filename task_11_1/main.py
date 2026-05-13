from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, conint
import uuid

app = FastAPI()

cats_db = dict()

class CatIn(BaseModel):
    name: str
    age: conint(gt=0)
    breed: str
    color: str
    vaccinated: bool

class CatOut(CatIn):
    id: str

@app.post('/cats', response_model=CatOut, status_code=201)
def register_cat(cat: CatIn):
    cat_id = str(uuid.uuid4())
    cats_db[cat_id] = cat.model_dump()
    return CatOut(id=cat_id, **cat.model_dump())

@app.get('/cats', status_code=200)
def get_all():
    result = []
    for cat_id, cat_data in cats_db.items():
        result.append(CatOut(id=cat_id, **cat_data).model_dump())
    return result

@app.get('/cats/{cat_id}', response_model=CatOut, status_code=200)
def get_cat(cat_id: str):
    if cat_id not in cats_db:
        raise HTTPException(status_code=404, detail="Cat not found")
    return CatOut(id=cat_id, **cats_db[cat_id])

@app.delete('/cats/{cat_id}', status_code=204)
def delete_cat(cat_id: str):
    if cat_id not in cats_db:
        raise HTTPException(status_code=404, detail="Cat not found")
    cats_db.pop(cat_id)
    return Response(status_code=204)

