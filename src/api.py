import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from crewai import Crew, Process
from src.agents.rca_agents import RCAAgents
from src.agents.rca_tasks import RCATasks

load_dotenv()

app = FastAPI(title="RCA Agent API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class IncidentRequest(BaseModel):
    log_group_name: str
    namespace: str
    metric_name: str
    dimension_name: str
    dimension_value: str
    minutes_ago: int = 60

# Global state to store latest analysis (in-memory for demo purposes)
# In production, this would be a database
latest_analysis = {"status": "idle", "result": None}

def run_rca_crew(incident_request: IncidentRequest):
    global latest_analysis
    latest_analysis["status"] = "running"
    
    try:
        # Convert Pydantic model to dict
        incident_context = incident_request.model_dump()
        
        agents = RCAAgents()
        tasks = RCATasks()

        detective = agents.detective_agent()
        auditor = agents.auditor_agent()
        sre = agents.sre_agent()
        remediator = agents.remediation_agent()

        task1 = tasks.gather_logs_metrics_task(detective, incident_context)
        task2 = tasks.audit_changes_task(auditor, incident_context)
        task3 = tasks.root_cause_analysis_task(sre, [task1, task2])
        task4 = tasks.remediation_plan_task(remediator, [task3])

        rca_crew = Crew(
            agents=[detective, auditor, sre, remediator],
            tasks=[task1, task2, task3, task4],
            verbose=True,
            process=Process.sequential
        )

        result = rca_crew.kickoff()
        latest_analysis["status"] = "completed"
        latest_analysis["result"] = str(result)
        
    except Exception as e:
        latest_analysis["status"] = "failed"
        latest_analysis["result"] = str(e)
        print(f"RCA Failed: {e}")

@app.get("/")
def read_root():
    return {"status": "Active", "service": "RCA-Agent"}

@app.post("/investigate")
def start_investigation(request: IncidentRequest, background_tasks: BackgroundTasks):
    if latest_analysis["status"] == "running":
        raise HTTPException(status_code=409, detail="Analysis already running")
    
    background_tasks.add_task(run_rca_crew, request)
    return {"message": "Investigation started", "status": "running"}

@app.get("/status")
def get_status():
    return latest_analysis

@app.get("/inventory")
def get_inventory():
    # Mocked inventory for dashboard visualization
    # In real implementation, this would call AWS Resource Groups Tagging API
    return {
        "resources": [
            {"id": "i-1234567890abcdef0", "type": "EC2", "status": "healthy", "region": "us-east-1"},
            {"id": "db-production-primary", "type": "RDS", "status": "healthy", "region": "us-east-1"},
            {"id": "production-api-service", "type": "Lambda", "status": "warning", "region": "us-east-1"}, # The failing one
            {"id": "queue-processing-worker", "type": "ECS", "status": "healthy", "region": "us-east-1"},
        ]
    }
