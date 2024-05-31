from fastapi import FastAPI
from model import controller

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/explain/{term}")
def explain(term: str):
    return controller.explain(term)

@app.get("/define/{term}")
def define(term: str):
    return controller.define(term)

@ app.get("/identify/{text}")
def identify(text: str):
    return controller.identify(text)

@ app.get("/identify_llm/{text}")
def identify(text: str):
    return controller.identify_llm(text)