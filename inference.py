from dotenv import load_dotenv
load_dotenv()
import os
import json
from openai import OpenAI
from environment import ProjectApprovalEnv
from models import Action

# Use environment variables - no defaults for security
API_KEY = os.environ["API_KEY"]
MODEL_NAME = os.environ["MODEL_NAME"]
API_BASE_URL = os.environ["API_BASE_URL"]
BENCHMARK = "project-approval"

client = OpenAI(api_key=API_KEY, base_url=API_BASE_URL)
env = ProjectApprovalEnv()
total_rewards = []

for level in ["easy", "medium", "hard"]:
    print(f"[START] task={level} env={BENCHMARK} model={MODEL_NAME}", flush=True)
    obs = env.reset(level)
    observation_data = {
        "project_id": obs.project_id,
        "title": obs.title,
        "budget": obs.budget,
        "risk_level": obs.risk_level,
        "status": obs.status,
        "completeness": obs.completeness
    }

    prompt = f"""You are a project approval agent. Make a decision based on these rules:
- If completeness > 0.8 AND risk_level is low -> decide: approve
- If completeness < 0.5 OR risk_level is high -> decide: reject
- If risk_level is high -> decide: reject
- Otherwise -> decide: request_changes

Project: {json.dumps(observation_data)}

Respond with ONLY one word: approve, reject, or request_changes"""

    error = None
    decision = "request_changes"
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
        error = str(e)

    action = Action(decision=decision)
    obs, reward, done, _ = env.step(action)

    error_val = error if error else "null"
    print(f"[STEP] step=1 action={decision} reward={reward.score:.2f} done=true error={error_val}", flush=True)

    score = reward.score
    total_rewards.append(score)
    success = score >= 0.5
    print(f"[END] success={str(success).lower()} steps=1 score={score:.3f} rewards={score:.2f}", flush=True)
