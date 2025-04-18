
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4

app = FastAPI()

# In-Memory Data Stores (Prototype Only)
agents = {}
tasks = {}

# Models
class Task(BaseModel):
    id: str
    title: str
    description: Optional[str] = ""
    assigned_agent: str
    division: str
    status: str = "pending"

class Agent(BaseModel):
    id: str
    name: str
    role: str
    divisions: List[str]

class RunTaskRequest(BaseModel):
    title: str
    description: Optional[str] = ""
    assigned_agent: str
    division: str

# Routes
@app.post("/agents")
def register_agent(agent: Agent):
    agents[agent.id] = agent
    return {"message": "Agent registered successfully."}

@app.post("/tasks/run")
def run_task(task_req: RunTaskRequest):
    task_id = str(uuid4())
    task = Task(
        id=task_id,
        title=task_req.title,
        description=task_req.description,
        assigned_agent=task_req.assigned_agent,
        division=task_req.division,
        status="assigned"
    )
    tasks[task_id] = task
    return {"message": "Task assigned.", "task_id": task_id}

@app.get("/tasks/{task_id}")
def get_task_status(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]

@app.post("/tasks/{task_id}/update")
def update_task_status(task_id: str, status: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks[task_id].status = status
    return {"message": "Task status updated.", "status": status}

# Example agent registration for testing
@app.on_event("startup")
def setup_initial_agents():
    agents["ana"] = Agent(id="ana", name="Ana", role="Systems Architect", divisions=["core", "rituals"])
    agents["zuberi"] = Agent(id="zuberi", name="Zuberi", role="GM", divisions=["core", "commerce"])
    agents["maya"] = Agent(id="maya", name="Maya", role="Designer", divisions=["gallery", "rituals"])
    agents["kofi"] = Agent(id="kofi", name="Kofi", role="Marketing Strategist", divisions=["commerce", "launch"])
    agents["oracle"] = Agent(id="oracle", name="The Oracle", role="Advisor", divisions=["vision", "research"])
