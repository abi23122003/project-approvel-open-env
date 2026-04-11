import os
import json
from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse
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

@app.get("/", response_class=HTMLResponse)
def root():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Approval OpenEnv</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Segoe UI', sans-serif; background: #0f172a; color: #e2e8f0; min-height: 100vh; padding: 20px; }
        h1 { text-align: center; color: #38bdf8; margin-bottom: 8px; font-size: 2rem; }
        .subtitle { text-align: center; color: #94a3b8; margin-bottom: 30px; }
        .container { max-width: 900px; margin: 0 auto; }
        .card { background: #1e293b; border-radius: 12px; padding: 20px; margin-bottom: 20px; border: 1px solid #334155; }
        .card h2 { color: #38bdf8; margin-bottom: 15px; font-size: 1.1rem; }
        .controls { display: flex; gap: 10px; flex-wrap: wrap; align-items: center; }
        select, button { padding: 10px 18px; border-radius: 8px; border: none; font-size: 0.95rem; cursor: pointer; }
        select { background: #0f172a; color: #e2e8f0; border: 1px solid #475569; }
        button { background: #0284c7; color: white; font-weight: 600; transition: background 0.2s; }
        button:hover { background: #0369a1; }
        button.approve { background: #16a34a; }
        button.approve:hover { background: #15803d; }
        button.reject { background: #dc2626; }
        button.reject:hover { background: #b91c1c; }
        button.changes { background: #d97706; }
        button.changes:hover { background: #b45309; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; }
        .stat { background: #0f172a; border-radius: 8px; padding: 14px; border: 1px solid #334155; }
        .stat-label { color: #94a3b8; font-size: 0.8rem; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.05em; }
        .stat-value { font-size: 1.3rem; font-weight: 700; color: #f1f5f9; }
        .badge { display: inline-block; padding: 3px 10px; border-radius: 999px; font-size: 0.8rem; font-weight: 600; }
        .badge-low { background: #166534; color: #bbf7d0; }
        .badge-medium { background: #854d0e; color: #fef08a; }
        .badge-high { background: #991b1b; color: #fecaca; }
        .badge-pending { background: #1e40af; color: #bfdbfe; }
        .badge-approved { background: #166534; color: #bbf7d0; }
        .badge-rejected { background: #991b1b; color: #fecaca; }
        .log { background: #0f172a; border-radius: 8px; padding: 14px; font-family: monospace; font-size: 0.85rem; max-height: 200px; overflow-y: auto; border: 1px solid #334155; }
        .log-entry { padding: 4px 0; border-bottom: 1px solid #1e293b; color: #94a3b8; }
        .log-entry.good { color: #4ade80; }
        .log-entry.bad { color: #f87171; }
        .reward-bar { height: 8px; background: #0f172a; border-radius: 4px; margin-top: 8px; overflow: hidden; }
        .reward-fill { height: 100%; background: linear-gradient(90deg, #ef4444, #eab308, #22c55e); border-radius: 4px; transition: width 0.4s; }
        #status-msg { text-align: center; padding: 10px; border-radius: 8px; margin-top: 10px; display: none; }
        .msg-good { background: #14532d; color: #86efac; }
        .msg-bad { background: #7f1d1d; color: #fca5a5; }
    </style>
</head>
<body>
<div class="container">
    <h1>🏛️ Project Approval OpenEnv</h1>
    <p class="subtitle">RL Environment for AI Project Decision Making</p>

    <div class="card">
        <h2>⚙️ Controls</h2>
        <div class="controls">
            <select id="difficulty">
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard</option>
            </select>
            <button onclick="resetEnv()">🔄 New Project</button>
            <button class="approve" onclick="makeDecision('approve')">✅ Approve</button>
            <button class="changes" onclick="makeDecision('request_changes')">✏️ Request Changes</button>
            <button class="reject" onclick="makeDecision('reject')">❌ Reject</button>
        </div>
        <div id="status-msg"></div>
    </div>

    <div class="card">
        <h2>📋 Current Project</h2>
        <div class="grid" id="project-grid">
            <div class="stat"><div class="stat-label">Project ID</div><div class="stat-value" id="project-id">—</div></div>
            <div class="stat"><div class="stat-label">Title</div><div class="stat-value" id="title" style="font-size:0.95rem">—</div></div>
            <div class="stat"><div class="stat-label">Budget</div><div class="stat-value" id="budget">—</div></div>
            <div class="stat"><div class="stat-label">Risk Level</div><div class="stat-value" id="risk">—</div></div>
            <div class="stat"><div class="stat-label">Status</div><div class="stat-value" id="status">—</div></div>
            <div class="stat"><div class="stat-label">Completeness</div><div class="stat-value" id="completeness">—</div></div>
        </div>
    </div>

    <div class="card">
        <h2>📊 Last Reward</h2>
        <div id="reward-display" style="font-size:2rem;font-weight:700;color:#38bdf8;">—</div>
        <div class="reward-bar"><div class="reward-fill" id="reward-bar" style="width:50%"></div></div>
    </div>

    <div class="card">
        <h2>📜 Decision Log</h2>
        <div class="log" id="log"><div class="log-entry">Start a new project to begin...</div></div>
    </div>
</div>

<script>
    let logEntries = [];

    function addLog(msg, type='') {
        logEntries.unshift({msg, type});
        if (logEntries.length > 50) logEntries.pop();
        const log = document.getElementById('log');
        log.innerHTML = logEntries.map(e => `<div class="log-entry ${e.type}">${e.msg}</div>`).join('');
    }

    function showStatus(msg, good=true) {
        const el = document.getElementById('status-msg');
        el.textContent = msg;
        el.className = good ? 'msg-good' : 'msg-bad';
        el.style.display = 'block';
        setTimeout(() => el.style.display = 'none', 3000);
    }

    function renderProject(obs) {
        document.getElementById('project-id').textContent = obs.project_id || '—';
        document.getElementById('title').textContent = obs.title || '—';
        document.getElementById('budget').textContent = obs.budget ? '$' + Number(obs.budget).toLocaleString() : '—';

        const risk = obs.risk_level || '';
        const riskClass = risk === 'low' ? 'badge-low' : risk === 'medium' ? 'badge-medium' : 'badge-high';
        document.getElementById('risk').innerHTML = `<span class="badge ${riskClass}">${risk}</span>`;

        const status = obs.status || '';
        const statusClass = status === 'approved' ? 'badge-approved' : status === 'rejected' ? 'badge-rejected' : 'badge-pending';
        document.getElementById('status').innerHTML = `<span class="badge ${statusClass}">${status}</span>`;

        const comp = obs.completeness != null ? Math.round(obs.completeness * 100) + '%' : '—';
        document.getElementById('completeness').textContent = comp;
    }

    async function resetEnv() {
        const diff = document.getElementById('difficulty').value;
        try {
            const res = await fetch('/reset?difficulty=' + diff, {method: 'POST'});
            const data = await res.json();
            renderProject(data);
            document.getElementById('reward-display').textContent = '—';
            document.getElementById('reward-bar').style.width = '50%';
            addLog(`[NEW] Project "${data.title}" loaded (${diff})`, 'good');
            showStatus('New project loaded!', true);
        } catch(e) {
            addLog('[ERROR] Failed to reset: ' + e.message, 'bad');
            showStatus('Error connecting to server', false);
        }
    }

    async function makeDecision(decision) {
        try {
            const res = await fetch('/step?decision=' + decision, {method: 'POST'});
            const data = await res.json();
            renderProject(data.observation);
            const reward = data.reward;
            document.getElementById('reward-display').textContent = reward >= 0 ? '+' + reward.toFixed(2) : reward.toFixed(2);
            const pct = Math.min(100, Math.max(0, (reward + 1) / 2 * 100));
            document.getElementById('reward-bar').style.width = pct + '%';
            const type = reward > 0 ? 'good' : reward < 0 ? 'bad' : '';
            addLog(`[${decision.toUpperCase()}] Reward: ${reward.toFixed(2)} | Done: ${data.done}`, type);
            if (data.done) showStatus('Episode done! Start a new project.', reward >= 0);
            else showStatus('Decision made: ' + decision, reward >= 0);
        } catch(e) {
            addLog('[ERROR] ' + e.message, 'bad');
            showStatus('Error — reset first?', false);
        }
    }

    // Auto-load on start
    resetEnv();
</script>
</body>
</html>
"""

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