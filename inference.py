from dotenv import load_dotenv
load_dotenv()
import os
import json
from openai import OpenAI
from environment import ProjectApprovalEnv
from models import Action

API_KEY = os.environ.get("API_KEY") or os.environ.get("OPENAI_API_KEY")
MODEL_NAME = os.environ.get("MODEL_NAME", "llama-3.1-8b-instant")
API_BASE_URL = os.environ.get("API_BASE_URL", "https://api.groq.com/openai/v1")

client = OpenAI(
    api_key=API_KEY,
    base_url=API_BASE_URL
)

print("[START]")
env = ProjectApprovalEnv()
total_reward = 0.0
task_count = 0

for level in ["easy", "medium", "hard"]:
    print(f"[STEP] task_difficulty={level}")
    obs = env.reset(level)
    observation_data = {
        "project_id": obs.project_id,
        "title": obs.title,
        "budget": obs.budget,
        "risk_level": obs.risk_level,
        "status": obs.status,
        "completeness": obs.completeness
    }
    print(f"[STEP] observation={json.dumps(observation_data)}")

    prompt = f"""You are a project approval agent. Make a decision based on these rules:
- If completeness > 0.8 AND risk_level is low -> decide: approve
- If completeness < 0.5 OR risk_level is high -> decide: reject
- Otherwise -> decide: request_changes

Project: {json.dumps(observation_data)}

Respond with ONLY one word: approve, reject, or request_changes"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            max_tokens=10,
            messages=[{"role": "user", "content": prompt}]
        )
        decision = response.choices[0].message.content.strip().lower()
        if decision not in ["approve", "reject", "request_changes"]:
            decision = "request_changes"
    except Exception as e:
        print(f"[STEP] error={str(e)}")
        decision = "request_changes"

    print(f"[STEP] decision={decision}")
    action = Action(decision=decision)
    obs, reward, done, _ = env.step(action)
    print(f"[STEP] reward={reward.score}")
    total_reward += reward.score
    task_count += 1

print(f"[STEP] total_reward={total_reward}")
print(f"[STEP] total_tasks={task_count}")
print(f"[STEP] average_reward={total_reward / task_count if task_count > 0 else 0}")
print("[END]")
