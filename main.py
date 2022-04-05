from fastapi import FastAPI
from bibs import java_test
import db

app = FastAPI()
db.get_db('db.sqlite')

@app.get("/")
async def root():
    return "ok"

