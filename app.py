import os
import json
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
from dotenv import load_dotenv
from environment import ProjectApprovalEnv
from models import Action

load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY") or os.environ.get("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.1-8b-instant")
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.groq.com/openai/v1")

app = FastAPI(title="Project Approval OpenEnv")

env = ProjectApprovalEnv()

@app.get("/")
def root():
    return {"status": "ok", "message": "Project Approval OpenEnv Running"}

@app.post("/reset")
def reset(difficulty: str = "easy"):
    obs = env.reset(difficulty)
    return JSONResponse(content={
        "project_id": obs.project_id,
        "title": obs.title,
        "budget": obs.budget,
        "risk_level": obs.risk_level,
        "status": obs.status,
        "completeness": obs.completeness
    })

@app.post("/step")
def step(decision: str = "request_changes"):
    action = Action(decision=decision)
    obs, reward, done, info = env.step(action)
    return JSONResponse(content={
        "observation": {
            "project_id": obs.project_id,
            "title": obs.title,
            "budget": obs.budget,
            "risk_level": obs.risk_level,
            "status": obs.status,
            "completeness": obs.completeness
        },
        "reward": reward.score,
        "done": done,
        "info": info
    })

@app.get("/state")
def state():
    return JSONResponse(content=env.state())

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
