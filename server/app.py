import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse
import uvicorn
from dotenv import load_dotenv
from environment import ProjectApprovalEnv
from models import Action

load_dotenv()

app = FastAPI(title="Project Approval OpenEnv")
env = ProjectApprovalEnv()

@app.get("/", response_class=HTMLResponse)
def root():
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Project Approval OpenEnv</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',sans-serif;background:#0f172a;color:#e2e8f0;min-height:100vh;padding:24px}
h1{text-align:center;color:#38bdf8;margin-bottom:6px;font-size:2rem}
.sub{text-align:center;color:#94a3b8;margin-bottom:28px}
.wrap{max-width:860px;margin:0 auto}
.card{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:18px;border:1px solid #334155}
.card h2{color:#38bdf8;margin-bottom:14px;font-size:1rem;text-transform:uppercase;letter-spacing:.05em}
.controls{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
select,button{padding:10px 18px;border-radius:8px;border:none;font-size:.95rem;cursor:pointer}
select{background:#0f172a;color:#e2e8f0;border:1px solid #475569}
button{background:#0284c7;color:#fff;font-weight:600;transition:background .2s}
button:hover{background:#0369a1}
.approve{background:#16a34a}.approve:hover{background:#15803d}
.reject{background:#dc2626}.reject:hover{background:#b91c1c}
.changes{background:#d97706}.changes:hover{background:#b45309}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin-top:4px}
.stat{background:#0f172a;border-radius:8px;padding:14px;border:1px solid #334155}
.slabel{color:#94a3b8;font-size:.75rem;text-transform:uppercase;letter-spacing:.05em;margin-bottom:4px}
.sval{font-size:1.25rem;font-weight:700;color:#f1f5f9}
.badge{display:inline-block;padding:3px 10px;border-radius:999px;font-size:.8rem;font-weight:600}
.low{background:#166534;color:#bbf7d0}.medium{background:#854d0e;color:#fef08a}.high{background:#991b1b;color:#fecaca}
.pending{background:#1e40af;color:#bfdbfe}.approved{background:#166534;color:#bbf7d0}.rejected{background:#991b1b;color:#fecaca}
.rbar{height:10px;background:#0f172a;border-radius:5px;margin-top:10px;overflow:hidden;border:1px solid #334155}
.rfill{height:100%;background:linear-gradient(90deg,#ef4444,#eab308,#22c55e);border-radius:5px;transition:width .4s}
.log{background:#0f172a;border-radius:8px;padding:14px;font-family:monospace;font-size:.82rem;max-height:180px;overflow-y:auto;border:1px solid #334155}
.le{padding:3px 0;border-bottom:1px solid #1e293b;color:#64748b}
.le.g{color:#4ade80}.le.b{color:#f87171}
#msg{text-align:center;padding:9px;border-radius:8px;margin-top:12px;display:none;font-weight:600}
.mg{background:#14532d;color:#86efac}.mb{background:#7f1d1d;color:#fca5a5}
</style>
</head>
<body>
<div class="wrap">
<h1>&#127963; Project Approval OpenEnv</h1>
<p class="sub">RL Environment for AI Project Decision Making</p>
<div class="card">
<h2>&#9881; Controls</h2>
<div class="controls">
<select id="diff"><option value="easy">Easy</option><option value="medium">Medium</option><option value="hard">Hard</option></select>
<button onclick="resetEnv()">&#128260; New Project</button>
<button class="approve" onclick="decide('approve')">&#9989; Approve</button>
<button class="changes" onclick="decide('request_changes')">&#9998; Request Changes</button>
<button class="reject" onclick="decide('reject')">&#10060; Reject</button>
</div>
<div id="msg"></div>
</div>
<div class="card">
<h2>&#128203; Current Project</h2>
<div class="grid">
<div class="stat"><div class="slabel">Project ID</div><div class="sval" id="pid">-</div></div>
<div class="stat"><div class="slabel">Title</div><div class="sval" id="ptitle" style="font-size:.95rem">-</div></div>
<div class="stat"><div class="slabel">Budget</div><div class="sval" id="pbudget">-</div></div>
<div class="stat"><div class="slabel">Risk Level</div><div class="sval" id="prisk">-</div></div>
<div class="stat"><div class="slabel">Status</div><div class="sval" id="pstatus">-</div></div>
<div class="stat"><div class="slabel">Completeness</div><div class="sval" id="pcomp">-</div></div>
</div>
</div>
<div class="card">
<h2>&#128200; Last Reward</h2>
<div id="reward" style="font-size:2.2rem;font-weight:800;color:#38bdf8">-</div>
<div class="rbar"><div class="rfill" id="rbar" style="width:50%"></div></div>
</div>
<div class="card">
<h2>&#128220; Decision Log</h2>
<div class="log" id="log"><div class="le">Start a new project to begin...</div></div>
</div>
</div>
<script>
var logs=[];
function addLog(m,t){logs.unshift({m:m,t:t});if(logs.length>50)logs.pop();document.getElementById('log').innerHTML=logs.map(function(e){return'<div class="le '+e.t+'">'+e.m+'</div>'}).join('')}
function showMsg(m,g){var e=document.getElementById('msg');e.textContent=m;e.className=g?'mg':'mb';e.style.display='block';setTimeout(function(){e.style.display='none'},3000)}
function render(o){
document.getElementById('pid').textContent=o.project_id||'-';
document.getElementById('ptitle').textContent=o.title||'-';
document.getElementById('pbudget').textContent=o.budget?'$'+Number(o.budget).toLocaleString():'-';
var r=o.risk_level||'';document.getElementById('prisk').innerHTML='<span class="badge '+r+'">'+r+'</span>';
var s=o.status||'';document.getElementById('pstatus').innerHTML='<span class="badge '+s+'">'+s+'</span>';
document.getElementById('pcomp').textContent=o.completeness!=null?Math.round(o.completeness*100)+'%':'-';
}
function resetEnv(){
fetch('/reset?difficulty='+document.getElementById('diff').value,{method:'POST'})
.then(function(r){return r.json()})
.then(function(d){render(d);document.getElementById('reward').textContent='-';document.getElementById('rbar').style.width='50%';addLog('[NEW] "'+d.title+'" loaded','g');showMsg('New project loaded!',true)})
.catch(function(e){addLog('[ERROR] '+e.message,'b');showMsg('Connection error',false)})}
function decide(dec){
fetch('/step?decision='+dec,{method:'POST'})
.then(function(r){return r.json()})
.then(function(d){render(d.observation);var rw=d.reward;document.getElementById('reward').textContent=(rw>=0?'+':'')+rw.toFixed(2);document.getElementById('rbar').style.width=Math.min(100,Math.max(0,(rw+1)/2*100))+'%';addLog('['+dec.toUpperCase()+'] reward:'+rw.toFixed(2)+' done:'+d.done,rw>0?'g':rw<0?'b':'');if(d.done)showMsg('Episode done! Load new project.',rw>=0);else showMsg('Decision: '+dec,rw>=0)})
.catch(function(e){addLog('[ERROR] '+e.message,'b');showMsg('Error - try New Project first',false)})}
resetEnv();
</script>
</body></html>"""
    return HTMLResponse(content=html)

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
    