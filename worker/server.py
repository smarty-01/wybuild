import os,shutil,subprocess,tempfile,uuid
from pathlib import Path
from fastapi import FastAPI,Header,HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
app=FastAPI();TOKEN=os.getenv("WORKER_TOKEN","");ART=Path(os.getenv("ARTIFACT_DIR","/artifacts"));ART.mkdir(parents=True,exist_ok=True);JOBS={}
class Job(BaseModel):id:str|None=None;source:str;ref:str="main";name:str="App";version:str="1.0.0";output:str="apk"
def auth(a): 
 if TOKEN and a!=f"Bearer {TOKEN}":raise HTTPException(401,"Unauthorized")
def run(c,cwd,t=900):
 p=subprocess.run(c,cwd=cwd,text=True,capture_output=True,timeout=t)
 if p.returncode:raise RuntimeError((p.stdout+p.stderr)[-10000:])
@app.get("/health")
def health():return {"ok":True}
@app.post("/build")
def build(j:Job,authorization:str|None=Header(None)):
 auth(authorization);jid=j.id or str(uuid.uuid4());w=Path(tempfile.mkdtemp(prefix="forge-"));JOBS[jid]={"id":jid,"status":"building"}
 try:
  if not j.source.startswith("https://github.com/"):raise ValueError("Only HTTPS GitHub sources are allowed")
  run(["git","clone","--depth","1","--branch",j.ref,j.source,str(w)],str(w.parent),300)
  g=w/"gradlew"
  if not g.exists():raise RuntimeError("gradlew not found")
  g.chmod(0o700);task="bundleRelease" if j.output.lower()=="aab" else "assembleRelease";run([str(g),task,"--no-daemon"],str(w),900)
  patterns=["**/build/outputs/**/*.apk"] if task.startswith("assemble") else ["**/build/outputs/**/*.aab"]
  found=[] 
  for pat in patterns:found+=list(w.glob(pat))
  if not found:raise RuntimeError("No build artifact found")
  dest=ART/f"{jid}-{found[0].name}";shutil.copy2(found[0],dest);JOBS[jid]={"id":jid,"status":"success","filename":found[0].name,"artifact":str(dest)}
  return {"id":jid,"status":"success","filename":found[0].name,"download":f"/artifacts/{jid}"}
 except Exception as e:JOBS[jid]={"id":jid,"status":"failed","error":str(e)};return JOBS[jid]
 finally:shutil.rmtree(w,ignore_errors=True)
@app.get("/build/{jid}")
def status(jid,authorization:str|None=Header(None)):auth(authorization);return JOBS.get(jid,{"status":"unknown"})
@app.get("/artifacts/{jid}")
def artifact(jid,authorization:str|None=Header(None)):auth(authorization);j=JOBS.get(jid); 
 if not j or j.get("status")!="success":raise HTTPException(404,"Unavailable")
 return FileResponse(j["artifact"],filename=j["filename"],media_type="application/octet-stream")
