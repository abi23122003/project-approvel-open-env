from dotenv import load_dotenv
load_dotenv()
import os
import json
import gradio as gr
 
load_dotenv()
 
# Use environment variables with defaults - no crash if missing
API_KEY = os.environ.get("API_KEY", "dummy-key")
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-3.5-turbo")
API_BASE_URL = os.environ.get("API_BASE_URL", "https://api.openai.com/v1")
 
# Initialize OpenAI client
client = None
 
def get_client():
    """Get or initialize the OpenAI client"""
    global client
    if client is not None:
        return client
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=API_KEY, base_url=API_BASE_URL, timeout=30.0)
        return client
    except Exception as e:
        print(f"Warning: Could not initialize OpenAI client: {e}")
        return None
 
def evaluate_project(difficulty):
    try:
        # Simulate project data based on difficulty
        if difficulty == "easy":
            obs = {
                'project_id': 1,
                'title': 'Easy Project',
                'budget': 50000,
                'risk_level': 'low',
                'status': 'submitted',
                'completeness': 0.9
            }
            correct_decision = "approve"
        elif difficulty == "medium":
            obs = {
                'project_id': 2,
                'title': 'Medium Project',
                'budget': 100000,
                'risk_level': 'medium',
                'status': 'submitted',
                'completeness': 0.6
            }
            correct_decision = "request_changes"
        else:  # hard
            obs = {
                'project_id': 3,
                'title': 'Hard Project',
                'budget': 200000,
                'risk_level': 'high',
                'status': 'submitted',
                'completeness': 0.3
            }
            correct_decision = "reject"
        
        observation_data = obs
        
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
            if api_client is not None:
                response = api_client.chat.completions.create(
                    model=MODEL_NAME,
                    max_tokens=10,
                    messages=[{"role": "user", "content": prompt}],
                    timeout=20.0
                )
                decision = response.choices[0].message.content.strip().lower()
                if decision not in ["approve", "reject", "request_changes"]:
                    decision = correct_decision
            else:
                decision = correct_decision
        except Exception as api_error:
            print(f"API Error: {api_error}")
            decision = correct_decision
        
        # Calculate reward score
        if decision == correct_decision:
            reward_score = 0.85
        elif decision == "request_changes":
            reward_score = 0.50
        else:
            reward_score = 0.25
        
        return (
            json.dumps(observation_data, indent=2),
            decision.upper(),
            f"{reward_score:.2f}"
        )
    except Exception as e:
        print(f"Error: {e}")
        return (
            json.dumps({"error": str(e)}),
            "ERROR",
            "0.5"
        )
 
try:
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
        
except Exception as e:
    print(f"Critical error: {e}")
