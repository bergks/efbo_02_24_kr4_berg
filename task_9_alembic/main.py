from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Alembic migration task with PostgreSQL"}