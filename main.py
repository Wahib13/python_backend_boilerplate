from common import tasks
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    task = tasks.add.delay(1, 2)
    return {"message": f"hello world {task.id}"}


@app.get("/items/{item_id}")
async def item(item_id: int):
    return {"item_id": item_id}
