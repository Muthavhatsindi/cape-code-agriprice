from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, PlainTextResponse
from pydantic import BaseModel
from app.database import init_db
from app.ussd import process_ussd

app = FastAPI(title="African Farmer Market USSD", version="1.0.0")

@app.on_event("startup")
def startup():
    init_db()

@app.get("/", response_class=HTMLResponse)
def simulator():
    return HTML

@app.get("/health")
def health():
    return {"status": "ok", "service": "African Farmer Market USSD"}

@app.post("/ussd", response_class=PlainTextResponse)
async def ussd_callback(
    sessionId: str = Form(...),
    serviceCode: str = Form(...),
    phoneNumber: str = Form(...),
    text: str = Form("")
):
    # Africa's Talking sends form-encoded fields.
    return process_ussd(sessionId, text)

class SimulateRequest(BaseModel):
    session_id: str
    text: str

@app.post("/simulate")
def simulate(payload: SimulateRequest):
    return {"response": process_ussd(payload.session_id, payload.text)}

HTML = r"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Farm Market USSD Simulator</title>
<style>
body{font-family:Arial,sans-serif;background:#eef3ef;margin:0;padding:24px;color:#17352a}
.wrap{max-width:460px;margin:0 auto}.phone{background:#17352a;border-radius:28px;padding:18px;box-shadow:0 12px 35px #0002}
.top{color:#b9e6cf;font-size:12px;display:flex;justify-content:space-between;margin-bottom:14px}
.screen{background:#fff;border-radius:12px;min-height:250px;padding:20px;white-space:pre-wrap;line-height:1.6;font-family:monospace}
h1{font-size:22px}.hint{font-size:13px;color:#64746b}
.controls{display:flex;gap:8px;margin-top:12px}.controls input{flex:1;min-width:0;padding:12px;border-radius:8px;border:1px solid #aab8af;font-size:16px}
button{padding:12px 16px;border:0;border-radius:8px;background:#26734d;color:white;font-weight:bold;cursor:pointer}
.secondary{background:#64746b;margin-top:10px;width:100%}
</style>
</head>
<body><div class="wrap">
<h1>🌱 Farm Market USSD</h1><p class="hint">Interactive demonstration. Prices are sample data, not live market quotes.</p>
<div class="phone"><div class="top"><span>*120*456#</span><span>● Network</span></div>
<div id="screen" class="screen">Connecting to Farm Market…</div>
<div class="controls"><input id="choice" inputmode="numeric" maxlength="2" placeholder="Enter option"><button onclick="sendChoice()">Send</button></div>
<button class="secondary" onclick="restart()">Restart session</button></div>
<p class="hint">This simulator calls the same backend logic as the USSD callback.</p>
</div>
<script>
let sessionId="demo-"+Math.random().toString(36).slice(2);
let path=[];
async function callBackend(){
 const response=await fetch("/simulate",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({session_id:sessionId,text:path.join("*")})});
 const data=await response.json();
 document.getElementById("screen").textContent=data.response;
 document.getElementById("choice").value="";
}
async function sendChoice(){
 const value=document.getElementById("choice").value.trim();
 if(!value)return;
 path.push(value);
 await callBackend();
}
async function restart(){sessionId="demo-"+Math.random().toString(36).slice(2);path=[];await callBackend();}
document.getElementById("choice").addEventListener("keydown",e=>{if(e.key==="Enter")sendChoice()});
callBackend();
</script></body></html>
"""
