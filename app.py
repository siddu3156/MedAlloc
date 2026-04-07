from fastapi import FastAPI
import random

app = FastAPI()

state_data = {"patients": 5, "doctors": 2}

@app.get("/")
def home():
    return {"status": "running"}

@app.get("/reset")
def reset():
    global state_data
    state_data = {"patients": 5, "doctors": 2}
    return state_data

@app.post("/step")
def step(action: dict):
    global state_data
    
    reward = random.uniform(0, 1)
    state_data["patients"] = max(0, state_data["patients"] - 1)
    
    return {
        "state": state_data,
        "reward": reward,
        "done": state_data["patients"] == 0
    }

@app.get("/state")
def state():
    return state_data