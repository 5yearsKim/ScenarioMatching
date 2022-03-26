from fastapi import FastAPI
from pydantic import BaseModel

from grammerlib import grammer_check
from myscript import Scripter
from config import *
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scripter = Scripter(SCENARIO_MAP)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/check_grammer/")
async def check_grammer(sentence: str):
    matches = grammer_check(sentence)
    return matches

@app.get("/script_info/{script_id}")
async def script_info(script_id: str):
    info = scripter.get_info(script_id)
    return info

class ScoreIn(BaseModel):
    answer: str
    candidates: list = []

@app.post("/score_answer")
async def score_answer(body: ScoreIn):
    scores = scripter.score_answer(body.answer, body.candidates)
    return scores


class ScriptIn(BaseModel):
    turn_idx: int = 0
    trial: int = 0
    answer: str

@app.post("/script_respond/{script_id}")
async def script_respond(script_id: str, body: ScriptIn):
    rsp = scripter.respond(script_id, body.turn_idx, body.answer, body.trial)
    return rsp

if __name__ == "__main__":
    import uvicorn
    # uvicorn.run("app.app:app",host='0.0.0.0', port=4557, reload=True, debug=True, workers=3)
    uvicorn.run("deploy:app", host='0.0.0.0', port=8001, reload=False, debug=False, workers=2)

