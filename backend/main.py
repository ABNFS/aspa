from fastapi import FastAPI
from conta.controller import app as conta


app = FastAPI()
app.mount("/conta", conta)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
