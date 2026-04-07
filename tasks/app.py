from fastapi import FastAPI
from medalloc_env import MedAllocEnv

app = FastAPI()

env = MedAllocEnv()

@app.get("/reset")
def reset():
    return env.reset()

@app.post("/step")
def step(action: dict):
    return env.step(action)

@app.get("/state")
def state():
    return env.state()