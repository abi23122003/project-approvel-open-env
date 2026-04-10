from dotenv import load_dotenv
load_dotenv()
import os
import json
import gradio as gr
from dotenv import load_dotenv
from environment import ProjectApprovalEnv
from models import Action

load_dotenv()

# Get API keys but don't initialize clients yet - will initialize lazily when needed
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
USE_GROQ = GROQ_API_KEY is not None and os.getenv("USE_GROQ", "true").lower() == "true"

# Default model names
MODEL_NAME = os.getenv("MODEL_NAME", "mixtral-8x7b-32768" if USE_GROQ else "gpt-3.5-turbo")
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")

# Lazy-initialized clients
client = None

def get_client():
    """Get or initialize the API client lazily"""
    global client
    if client is not None:
        return client
    
    if USE_GROQ and GROQ_API_KEY:
        from groq import Groq
        client = Groq(api_key=GROQ_API_KEY)
    elif OPENAI_API_KEY:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY, base_url=API_BASE_URL, timeout=30.0)
    else:
        raise ValueError("No API credentials configured. Set GROQ_API_KEY or OPENAI_API_KEY environment variable.")
    
    return client

def evaluate_project(difficulty):
    try:
        env = ProjectApprovalEnv()
        obs = env.reset(difficulty)
        
        observation_data = {
            'project_id': obs.project_id,
            'title': obs.title,
            'budget': obs.budget,
            'risk_level': obs.risk_level,
            'status': obs.status,
            'completeness': obs.completeness
        }
        
        prompt = f"""You are a project approval agent. Based on the project details, make a decision.

Project: {obs}

Rules:
- If completeness > 0.8 AND risk_level is 'low' → decide: approve
- If completeness < 0.5 OR risk_level is 'high' → decide: reject  
- Otherwise → decide: request_changes

Respond with ONLY one word: approve, reject, or request_changes"""
        
        decision = "request_changes"
        try:
            api_client = get_client()
            
            if USE_GROQ:
                response = api_client.chat.completions.create(
                    model=MODEL_NAME,
                    max_tokens=10,
                    messages=[{"role": "user", "content": prompt}]
                )
            else:
                response = api_client.chat.completions.create(
                    model=MODEL_NAME,
                    max_tokens=10,
                    messages=[{"role": "user", "content": prompt}],
                    timeout=20.0
                )
            decision = response.choices[0].message.content.strip().lower()
            if decision not in ["approve", "reject", "request_changes"]:
                decision = "request_changes"
        except Exception as api_error:
            print(f"API Error: {api_error}")
            decision = "request_changes"
        
        action = Action(decision=decision)
        obs, reward, done, _ = env.step(action)
        
        return (
            json.dumps(observation_data, indent=2),
            decision.upper(),
            f"{reward.score:.1f}"
        )
    except Exception as e:
        return (
            json.dumps({"error": str(e)}),
            "ERROR",
            "0.0"
        )

with gr.Blocks(title="Project Approval AI") as demo:
    gr.Markdown("# Project Approval Evaluation System")
    gr.Markdown("Evaluate project proposals using AI with different difficulty levels")
    
    with gr.Row():
        difficulty = gr.Radio(
            choices=["easy", "medium", "hard"],
            value="easy",
            label="Difficulty Level"
        )
    
    submit_btn = gr.Button("Evaluate Project", variant="primary")
    
    with gr.Row():
        project_info = gr.Textbox(label="Project Information", lines=6)
        decision_output = gr.Textbox(label="Decision")
        reward_output = gr.Textbox(label="Reward")
    
    submit_btn.click(
        fn=evaluate_project,
        inputs=[difficulty],
        outputs=[project_info, decision_output, reward_output]
    )

def main():
    return demo

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
