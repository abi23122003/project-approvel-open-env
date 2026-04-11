from dotenv import load_dotenv
load_dotenv()
import os
import json
from openai import OpenAI
from tasks.easy import get_easy_task
from tasks.medium import get_medium_task
from tasks.hard import get_hard_task
from models import Action

# Use environment variables - no defaults for security
API_KEY = os.environ["API_KEY"]
MODEL_NAME = os.environ["MODEL_NAME"]
API_BASE_URL = os.environ["API_BASE_URL"]
BENCHMARK = "project-approval"

client = OpenAI(api_key=API_KEY, base_url=API_BASE_URL)

# Collect all tasks with graders
tasks_list = [
    get_easy_task(),
    get_medium_task(),
    get_hard_task()
]

all_rewards = []
total_steps = 0

for task in tasks_list:
    task_name = task["name"]
    correct_decision = task["correct_decision"]
    grader = task["grader"]
    
    # Remove grader and correct_decision from observation data
    observation_data = {k: v for k, v in task.items() if k not in ["grader", "correct_decision", "name"]}
    
    print(f"[START] task={task_name} env={BENCHMARK} model={MODEL_NAME}", flush=True)
    
    prompt = f"""You are a project approval agent. Make a decision based on these rules:
- If completeness > 0.8 AND risk_level is low -> decide: approve
- If completeness < 0.5 OR risk_level is high -> decide: reject
- Otherwise -> decide: request_changes

Project: {json.dumps(observation_data)}

Respond with ONLY one word: approve, reject, or request_changes"""

    error = None
    prediction = "request_changes"
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            max_tokens=10,
            messages=[{"role": "user", "content": prompt}]
        )
        prediction = response.choices[0].message.content.strip().lower()
        if prediction not in ["approve", "reject", "request_changes"]:
            prediction = "request_changes"
    except Exception as e:
        error = str(e)
        prediction = "request_changes"
    
    # Calculate reward using grader
    reward = grader(prediction, correct_decision)
    all_rewards.append(reward)
    total_steps += 1
    
    error_val = error if error else "null"
    print(f"[STEP] step=1 action={prediction} reward={reward:.2f} done=true error={error_val}", flush=True)
    
    # Determine success (score >= 0.5)
    success = reward >= 0.5
    rewards_str = f"{reward:.2f}"
    print(f"[END] success={str(success).lower()} steps=1 score={reward:.3f} rewards={rewards_str}", flush=True)

# Final summary
print(f"\n# FINAL SUMMARY", flush=True)
print(f"Total tasks: {total_steps}", flush=True)
print(f"Total rewards: {sum(all_rewards):.2f}", flush=True)
print(f"Average score: {sum(all_rewards) / total_steps if total_steps > 0 else 0:.3f}", flush=True)
